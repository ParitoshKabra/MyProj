from .models import *
from rest_framework import serializers
from django.utils.timezone import now

class UserCreatedByForeignkey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return users.objects.filter(id=self.context['request'].user.id)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    commented_by = UserCreatedByForeignkey()
    card_comments = serializers.PrimaryKeyRelatedField(queryset=Cards.objects.all())
    class Meta:
        model = Comments
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    comments_in_card = CommentSerializer(many=True, read_only=True)
    created_by = UserCreatedByForeignkey()
    class Meta:
        model = Cards
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    list_cards = CardSerializer(many=True, read_only=True)
    lists_project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    class Meta:
        model = Lists
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_lists = ListSerializer(read_only=True, many=True)
    created_by = UserCreatedByForeignkey()
    class Meta:
        model = Projects
        fields = '__all__'

class UserProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Projects
        fields = ['title', 'descp', 'id']

# create a better serializer structure        

class UserCardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cards
        fields = ['title', 'descp', 'id']

class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = users
        fields = ['username', 'id', 'is_staff', 'is_superuser', 'email']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    projects_of_user = UserProjectSerializer(many=True, read_only = True)
    comments_of_user = CommentSerializer(many=True, read_only=True)
    assigned_cards = UserCardSerializer(many=True, read_only=True)
    class Meta:
        model = users
        fields = ['id', 'username', 'projects_of_user','comments_of_user', 'assigned_cards', 'is_staff', 'is_superuser', 'email']



# same for members serializer
# assigned_to MemberSerializer()
# user vs users, use different serializers 
# change view or serializer , add creator to member 
# generic.ListApiViewSet and password issue