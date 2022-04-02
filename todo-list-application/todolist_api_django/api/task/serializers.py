from rest_framework import serializers
from api_auth.serializers import UserSerializer

from .models import Task

class TaskSerialzier(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = (
            'id',
            'user',
            'description',
            'status',
        )