from .models import *
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=254)
    
    def create(self, validate_data):
        """
        Create and return a new user_instance, based on validation
        """

        user =  users.objects.create(**validate_data)
        return user
    def update(self, instance, validate_data):
        """
        Update and return an existing instance based on the validation of data given
        """
        instance.username = validate_data.get('username', instance.username)
        instance.email = validate_data.get('email', instance.email)
        instance.save()
        return instance
class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Projects
        fields = '__all__'