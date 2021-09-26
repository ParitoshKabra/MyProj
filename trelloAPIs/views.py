import re
from django.contrib.auth.models import User
from django.http.response import Http404, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
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
auth_url_omniport = "https://channeli.in/oauth/authorise?client_id=9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"

class UserListApiViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = users.objects.all()
    serializer_class = UserListSerializer

class UserApiViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]

    def get_queryset(self):
        return users.objects.filter(id=self.request.user.id)
    

class ListApiViewSet(viewsets.ModelViewSet):
    queryset = Lists.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, ListPermissions]

class CardApiViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, CardPermissions]

    #on a post request put a check on users assigned and assign the creator to member of the project
    def get_permissions(self):
        if self.request.method == "POST":
            # print(self.request.method)
            # print("Came in post permissions")
            self.permission_classes =[IsAuthenticated, CardPermissions, CardAssignPermissionorAccess]
            # print(self.permission_classes)
        return super(CardApiViewSet, self).get_permissions()
    
class CommentApiViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanCommentorViewComments]

class ProjectApiViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]



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
        print(request.user.is_authenticated)
        res= Response({"success": msg}, status=status.HTTP_202_ACCEPTED)
        res['Access-Control-Allow-Origin']='http://127.0.0.1:3000'
        res['Access-Control-Allow-Credentials']= 'true'
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