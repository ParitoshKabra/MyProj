from django.contrib import admin
from django.urls import path, include
from . import views
from .routers import router
urlpatterns = [
    path('oauth_redirect', views.oauth_redirect, name='oauth_redirect'),
    path('login', views.trello_login, name='login_auth'),
    path('logout', views.log_out, name='logout'),
    path('check_login', views.check_login, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('csrf_token', views.get_csrf_token, name='csrf'),
    path('', include(router.urls)),
]
