import re
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http.response import Http404, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from .oauth import clientId, secret_token
from django.contrib.auth import login, authenticate, logout
from .oauth import exchange_code
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView, Response
from rest_framework import mixins, viewsets
from rest_framework import status
from .permissions import CanCommentorViewComments, CardAssignPermissionorAccess, CardPermissions, ListPermissions, ProjectPermission, UserPermissions
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync

auth_url_omniport = "https://channeli.in/oauth/authorise?client_id=9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"

class UserListApiViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = users.objects.all()
    serializer_class = UserListSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializer
        return super(UserListApiViewSet, self).get_serializer_class()
class UserApiViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    def get_queryset(self):
        if self.action == 'list':
            return users.objects.filter(id=self.request.user.id)
        else:
            return users.objects.all()
class ProjectMemberApiViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = ProjectMemberSerializer
    queryset = Projects.objects.all()

    

class ListApiViewSet(viewsets.ModelViewSet):
    queryset = Lists.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, ListPermissions]

class CardApiViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, CardPermissions]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return CardForCommentSerializer
        return super().get_serializer_class()
    #on a post request put a check on users assigned and assign the creator to member of the project
    def get_permissions(self):
        if self.request.method == "POST":
            # print(self.request.method)
            # print("Came in post permissions")
            self.permission_classes =[IsAuthenticated, CardPermissions, CardAssignPermissionorAccess]
            # print(self.permission_classes)
        return super(CardApiViewSet, self).get_permissions()

class ProjectMakeAdminViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Projects.objects.all()
    serializer_class = ProjectAdminSerializer
    permission_classes=[IsAuthenticatedOrReadOnly, ]

    def update(self, request, *args, **kwargs):
        print("called update method")
        partial = kwargs.pop('partial', False)
        
        instance = self.get_object()
        print(request.data)
        lt = []
        for item in request.data['admins']:
            lt.append(users.objects.get(id=item['id']))
        instance.admins.set(item for item in lt)
        instance.save()
        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

 
class CommentApiViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

class PostCommentApiViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Comments.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticated, CanCommentorViewComments]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = CommentSerializer(instance=instance)
        print(ser, ser.data)
        if instance.commented_by == request.user:
            self.perform_destroy(instance)
        else:
            return Response({"error": "comment can be modified only by its owner"}, status=status.HTTP_401_UNAUTHORIZED)
        async_to_sync(channel_layer.group_send)("comment_group", {"type": "delete_comment", "message":ser.data})
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if(instance.commented_by==request.user):
            self.perform_update(serializer)
        else:
            return Response({"error":"comment can be modified only by its creator"}, status=status.status.HTTP_400_BAD_REQUEST)
        ser = CommentSerializer(instance=instance)
        print(ser, ser.data)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        async_to_sync(channel_layer.group_send)("comment_group", {"type": "modified_comment", "message":ser.data})
        return Response(serializer.data)
        
class ProjectApiViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

    def create(self, request, *args, **kwargs):
        data_ = request.data
        print(data_)
        # data_._mutable = True
        creator = data_['created_by']
        data_['created_by'] = request.user.id
        members = data_.pop('members')
        admins = data_.pop('admins')
        b = self.check_creator(creator, members)
        if b:
            members.append(creator)
            data_['members'] = members
        b = self.check_creator(creator, admins)
        if b:
            admins.append(creator)
            data_['admins']= admins

        b1 = False
        for item in admins:
            if item not in members:
                b1 = True
        
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        if not b1:
            self.perform_create(serializer)
        else:
            return Response({"error": "admins must be members of the project"}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        members = request.data.get('members')
        print(members)
        if request.data['created_by'] not in members:
            print("error in members")
            return Response({"error": "can't remove creator of a project"}, status.HTTP_400_BAD_REQUEST)
         
        if request.data['created_by'] not in request.data.get('admins'):
            print("error in admins")
            return Response({"error": "creator can't be removed from admin"}, status.HTTP_400_BAD_REQUEST)         
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def check_creator(self, creator, *args ):
        for item in args:
            if item == creator:
                return False
        
        return True

    
@api_view(("GET", ))
def oauth_redirect(request):
    msg = "login already"
    if request.user.is_authenticated:
        return Response({"success": msg}, status=200)
    code = request.GET.get('code')
    user = exchange_code(code)
    if user is not None:
        user_ = authenticate(request=request, user_json=user)
        msg = "login success"
        login(request, user_) 
        res= Response({"success":"authentication successfull"}, status=status.HTTP_202_ACCEPTED)
        # res= Response({"sessionid": request.session._session_key, "csrftoken": get_token(request)}, status=status.HTTP_202_ACCEPTED)
        return res
    else:
        msg = "Invalid login credentials"
        return Response(msg,status=401)

def trello_login(request):
    if request.user.is_authenticated:
        return Response({"success": "loggedin"}, status=200)
    return redirect(auth_url_omniport)

def log_out(request):
    logout(request)
    return JsonResponse({"msg": "logged out successfully"})

@api_view(("POST", ))
def admin_login(request):
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    print(user)
    if user is not None:
        login(request, user)
        res = Response({"sessionid": request.session._session_key, "csrftoken": get_token(request)}, status=status.HTTP_202_ACCEPTED)
        return res
    else:
        return Response({"error": "user not found"}, status=status.HTTP_202_ACCEPTED)
@api_view(("GET",))
def get_csrf_token(request):
    return Response({"csrftoken":get_token(request)}, status=status.HTTP_202_ACCEPTED)
@api_view(("GET", ))
def check_login(request):
    msg = {
        "loggedin": True
    }
    if request.user.is_authenticated:
        return Response(msg, status=200)
    else:
        msg["loggedin"] = False
        return Response(msg, status=200)
