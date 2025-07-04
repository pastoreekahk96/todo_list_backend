from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# Serializer for the Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {

                'password': {'write_only': True}

                }  # Hide password in output

        def create(self, validated_data):
            user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
            )
            return user
