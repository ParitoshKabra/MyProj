from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/trelloAPIs/comments/(?P<pk>[0-9]+)/$', consumers.GetComment),
    re_path(r'ws/trelloAPIs/post_comments/(?P<pk>[0-9]+)/$', consumers.ModifyComment),
    re_path(r'ws/trelloAPIs/post_comments/$', consumers.PostComment),
]