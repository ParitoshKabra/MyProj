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
from rest_framework.views import APIView
from rest_framework import viewsets
from .permissions import CanCommentorViewComments, CardAssignPermissionorAccess, CardPermissions, ListPermissions, ProjectPermission, UserPermissions
auth_url_omniport = "https://channeli.in/oauth/authorise?client_id=9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"

class UserApiViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermissions]


class ListApiViewSet(viewsets.ModelViewSet):
    queryset = Lists.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, ListPermissions]

class CardApiViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, CardPermissions]

    def get_permissions(self):
        if self.request.method == "POST":
            print(self.request.method)
            print("Came in post permissions")
            self.permission_classes =[IsAuthenticated, CardPermissions, CardAssignPermissionorAccess]
            print(self.permission_classes)
        return super(CardApiViewSet, self).get_permissions()
    
class CommentApiViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanCommentorViewComments]

class ProjectApiViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermission]

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
def log_out(request):
    logout(request)
    return JsonResponse({"msg": "logged out successfully"})
