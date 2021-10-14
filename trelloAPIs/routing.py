from django.urls import re_path, path
from . import consumers
websocket_urlpatterns = [
    path('ws/test/', consumers.TestConsumer.as_asgi(), name='test_ws'),
    # re_path(r'trelloAPIs/comments/(?P<pk>[0-9]+)/$', consumers.GetComment),
    # re_path(r'trelloAPIs/post_comments/(?P<pk>[0-9]+)/$', consumers.ModifyComment),
    # re_path(r'trelloAPIs/post_comments/$', consumers.PostComment),
]