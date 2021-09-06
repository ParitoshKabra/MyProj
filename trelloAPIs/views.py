import re
from django.contrib.auth.models import User
from django.http.response import Http404, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
import requests
from .oauth import clientId, secret_token
from django.contrib.auth import login, authenticate
from .oauth import exchange_code
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import viewsets

auth_url_omniport = "https://channeli.in/oauth/authorise?client_id=9iXxR2JLU4HyfCi1umE5nDKTyjbpicWrFFUQPWAV"


@api_view(['GET'])
def get_all(request):
    print(request.user)
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
            return JsonResponse({"error_user_id":"user not found"})

    def put(self, request, pk): 
        if request.user.is_superuser:
            try:
                data = JSONParser().parse(request)
                obj = users.objects.get(id=pk)
                serializer = UserSerializer(obj,data=data)
                if serializer.is_valid():
                    serializer.save()
                    print(serializer.data)
                    return JsonResponse(serializer.data, status=202)
                return JsonResponse(serializer.errors, status=400)
            except users.DoesNotExist:
                return JsonResponse({"error_userid":"user not found"})
        else:
            return JsonResponse({"error_user_authorization": "You are not authorized to do so"})
    def delete(self, request, pk):
        try:
            task = users.objects.get(id=pk)
            task.delete()
            user = users.objects.all()
            serialized = UserSerializer(user, many=True)
            return JsonResponse(serialized.data, safe=False)
        except users.DoesNotExist:
            return JsonResponse({"errror_userid":"user not found"})

class UserApiViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserSerializer

class ProjectApiViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    def get_user_projects(self, request, pk):
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
    user_ = authenticate(request, user=user)
    if user_ is None:
        user_ = users.objects.create(
            id = user["userId"],
            username = user["person"]["fullName"],
            email = user["contactInformation"]["instituteWebmailAddress"]
        )
    msg = "success"
    login(request, user_)
    return redirect(f'/trelloAPIs/home/{msg}')

def trello_login(request):
    if request.user.is_authenticated:
        return redirect("/trelloAPIs/home/success")
    return redirect(auth_url_omniport)

@api_view(['GET', ])
@login_required(login_url='login_auth')
def get_user_projects(request, pk):
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
