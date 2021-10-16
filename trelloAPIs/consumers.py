import json
from django.core.exceptions import PermissionDenied
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Cards, Comments, users
from .serializers import CommentPostSerializer, UserListSerializer
from django.core import mail
connection = mail.get_connection()
connection.open()
class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "comment_group"
        print("Connection established successfully!!")
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # if self.scope['user'].is_authenticated and self.scope['user'].is_active:
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
        user_who_commented = await self.get_user_who_commented(message['commented_by'])
        assoc_card = await self.associated_card(message['card_comments'])
        assigned_users = await self.get_assigned_members(assoc_card, user_who_commented)
        
        email = await sync_to_async(mail.EmailMessage)(
            'Someone Commented On Your Card',
            f'This is an auto-genereated message to inform that {user_who_commented.username}, recently commented on the card {assoc_card.title}',
            'conquerorpk@gmail.com',
            assigned_users,
            connection=connection,
        )
        await self.send_email_(email)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'message': comment
            }
        )
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comment_group", self.channel_name)

    @sync_to_async
    def send_email_(self, email):
        email.send()
    async def comment_message(self, event):
        comment = event['message']
        await self.send(text_data=json.dumps({
            'info':'created',
            'comment': comment
        }))

    async def delete_comment(self, event):
        print("This was triggered!!")
        comment = event['message']
        await self.send(text_data=json.dumps({
            'info':'deleted',
            'comment': comment
        }))
    async def modified_comment(self, event):
        print("This was triggered when updated!!")
        comment = event['message']
        await self.send(text_data=json.dumps({
            'info':'modified',
            'comment': comment
        }))
    @database_sync_to_async
    def save_post(self, data):
        serializer = CommentPostSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        print(self.scope['user'].id, "user-id")
        print(data['commented_by'], self.scope['user'].id)
        
       
        x = serializer.create(serializer.validated_data)   

        data = CommentPostSerializer(x).data 
        usr = UserListSerializer(instance=users.objects.get(id=data['commented_by']))
        data['commented_by'] = usr.data
        return data
    @database_sync_to_async
    def get_user_who_commented(self, id):
        return users.objects.get(id=id)

    @database_sync_to_async
    def associated_card(self, id):
        return Cards.objects.get(id=id)
    @database_sync_to_async
    def get_assigned_members(self, instance, user):
        assigned_users=[]
        for members in instance.assigned_to.all():
            if members.email != '' and members != user:
                assigned_users.append(members.email)
        return assigned_users