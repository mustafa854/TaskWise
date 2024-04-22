from rest_framework import serializers
from core import models
from uuid import uuid4



class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, allow_blank=False)
    display_name = serializers.CharField(max_length=64, allow_blank=False)

class TeamSerializerView(serializers.Serializer):
    name = serializers.CharField(max_length=64, allow_blank=False)
    description = serializers.CharField(max_length=128)
    creation_time = serializers.CharField()
    admin = serializers.UUIDField()


class TeamSerializerCreateOrUpdate(serializers.Serializer):
    name = serializers.CharField(max_length=64, allow_blank=False)
    description = serializers.CharField(max_length=128)
    admin = serializers.UUIDField()


class BoardSerializerCreateOrUpdate(serializers.Serializer):
    name = serializers.CharField(max_length=64, allow_blank=False)
    description = serializers.CharField(max_length=128, allow_blank=True)
    team_id = serializers.UUIDField()
    
    
    
class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64, allow_blank=False)
    description = serializers.CharField(max_length=128, allow_blank=True)
    user_id = serializers.UUIDField()