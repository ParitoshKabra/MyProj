from django.contrib import admin
from django.urls import path, include
from . import views
from .routers import router
urlpatterns = [
    path('oauth_redirect', views.oauth_redirect, name='oauth_redirect'),
    path('login', views.trello_login, name='login_auth'),
    path('home/<str:msg>', views.home, name='home'),
    path('logout/', views.log_out, name='logout'),
    path('', include(router.urls)),
]
