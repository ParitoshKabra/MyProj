import json
from django.core.exceptions import PermissionDenied
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Comments, users
from .serializers import CommentPostSerializer, UserListSerializer

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "comment_group"
        print("Connection established successfully!!")
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        print(self.scope['user'], self.scope['url_route'])
        await self.accept()
        await self.send(text_data=json.dumps({"message":"Connection established successfully!!"}))
        # pass
    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        if int(message['commented_by']) != int(self.scope['user'].id):
            raise PermissionDenied("You cannot send comments on behalf of others")
        comment = await self.save_post(message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'message': comment
            }
        )
        pass
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comment_group", self.channel_name)

        pass

    async def comment_message(self, event):
        comment = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment': comment
        }))

    @database_sync_to_async
    def save_post(self, data):
        serializer = CommentPostSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        print(self.scope['user'].id, "user-id")
        print(data['commented_by'], self.scope['user'].id)
        
        # card not working + ui suxx on other browser + data issue and pagination + biggest issue: self.scope not a good thing
        x = serializer.create(serializer.validated_data)    #this will create the post

        data = CommentPostSerializer(x).data #this will return the serialized post data
        usr = UserListSerializer(instance=users.objects.get(id=data['commented_by']))
        data['commented_by'] = usr.data
        return data
# class PostComment(WebsocketConsumer):
#     pass
# class ModifyComment(WebsocketConsumer):
#     pass