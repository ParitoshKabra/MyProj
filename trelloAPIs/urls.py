from django.contrib import admin
from django.urls import path, include
from . import views
from .routers import router
urlpatterns = [
    path('user_all', views.get_all, name = 'user_all'),
    path('user/<int:pk>', views.UserApiView.as_view()),
    path('oauth_redirect', views.oauth_redirect, name='oauth_redirect'),
    path('login', views.trello_login, name='login_auth'),
    path('home/<str:msg>', views.home, name='home'),
    # path('user/<int:pk>/projects', views.get_user_projects, name='user_projects'),
    path('', include(router.urls)),
]
