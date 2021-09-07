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
from django.contrib.auth import login, authenticate
from .oauth import exchange_code
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from rest_framework import viewsets
from .permissions import CanCommentorViewComments, CardPermissions, ListPermissions, ProjectPermission, UserPermissions
auth_url_omniport = "https://channeli.in/oauth/authorise?client_id=9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"


@api_view(['GET'])
def get_all(request):
    users_ = users.objects.all()
    serializer = UserSerializer(users_, many=True)
    return JsonResponse(serializer.data, safe=False)

class UserApiView(APIView):
    def get(self, request, pk):
        try:
            user = users.objects.get(id=pk)
            serialized = UserSerializer(user, many=False)
            return JsonResponse(serialized.data, safe=False)
        except users.DoesNotExist:
            return JsonResponse({"error_user_id":"user not found"}, status=404)

    def put(self, request, pk): 
        if request.user.is_superuser:
            try:
                data = JSONParser().parse(request)
                obj = users.objects.get(id=pk)
                serializer = UserSerializer(obj,data=data)
                if serializer.is_valid():
                    serializer.save()
                    # print(serializer.data)
                    return JsonResponse(serializer.data, status=202)
                return JsonResponse(serializer.errors, status=400)
            except users.DoesNotExist:
                return JsonResponse({"error_userid":"user not found"})
        else:
            return JsonResponse({"error_user_authorization": "You are not authorized to do so"}, status=401)
    def delete(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            try:
                task = users.objects.get(id=pk)
                task.is_active = False
                task.save()
                user = users.objects.all()
                serialized = UserSerializer(user, many=True)
                return JsonResponse(serialized.data, safe=False)
            except users.DoesNotExist:
                return JsonResponse({"errror_userid":"user not found"})
        else:
            return JsonResponse({"error_user_authorization": "You are not authorized to do so"}, status=401)

class UserApiViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]


class ListApiViewSet(viewsets.ModelViewSet):
    queryset = Lists.objects.all()
    serializer_class = ListSerializer
    permission_classes = [ListPermissions, IsAuthenticated]

class CardApiViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [CardPermissions, IsAuthenticated]

    #permission associated with assigned_to field

class CommentApiViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CanCommentorViewComments,IsAuthenticated]

class ProjectApiViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission, ]
    
    @action(detail=True, methods=['get'], url_path='proj', url_name='projects-proj')
    def get_user_projects(self, request, pk=None):
        try:
            projects = Projects.objects.all()
            user_ = users.objects.get(id=pk)
            mydict = {"member_projects":{}, "creator_projects": {}}
            for item in projects:
                for member in item.members.iterator():
                    if user_.id == member.id:
                        mydict["member_projects"][item.id] =  item.title
                if item.created_by == user_:
                    mydict["creator_projects"][item.id]= item.title
            return JsonResponse(mydict)        
        except users.DoesNotExist:
            return JsonResponse({"error_user_id": "not found"})





@login_required(login_url="login_auth")
def home(request, msg):
    return JsonResponse({"msg": msg})

def oauth_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    user_ = authenticate(request=request, user_json=user)
    msg = "success"
    login(request, user_)
    return redirect(f'/trelloAPIs/home/{msg}')

def trello_login(request):
    if request.user.is_authenticated:
        return redirect("/trelloAPIs/home/success")
    return redirect(auth_url_omniport)

# @api_view(['GET', ])
# @login_required(login_url='login_auth')
# def get_user_projects(request, pk):
#     try:
#         projects = Projects.objects.all()
#         user_ = users.objects.get(id=pk)
#         mydict = {"member_projects":{}, "creator_projects": {}}
#         for item in projects:
#             for member in item.members.iterator():
#                 if user_.id == member.id:
#                     mydict["member_projects"][item.id] =  item.title
#             if item.created_by == user_:
#                 mydict["creator_projects"][item.id]= item.title
#         return JsonResponse(mydict)        
#     except users.DoesNotExist:
#         return JsonResponse({"error_user_id": "not found"})
