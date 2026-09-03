from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serialize tasks without allowing clients to change ownership."""

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    """Validate registration data and create users with hashed passwords."""

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
