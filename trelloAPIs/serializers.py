from .models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'

class UserCreatedByForeignkey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return users.objects.filter(id=self.context['request'].user.id)


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
    lists_project = serializers.PrimaryKeyRelatedField(read_only=True)
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

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    projects_of_user = ProjectSerializer(many=True, read_only = True)
    comments_of_user = CommentSerializer(many=True, read_only=True)
    assigned_cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = users
        fields = ['username', 'id', 'projects_of_user', 'is_staff', 'is_superuser', 'email', 'comments_of_user', 'assigned_cards']




