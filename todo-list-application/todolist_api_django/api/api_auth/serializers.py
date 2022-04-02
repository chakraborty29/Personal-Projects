from django.db import models
from rest_framework import serializers
from django.conf import settings

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            # 'firebase_id',
            'is_superuser',
            'is_staff',
            'username',
            'first_name',
            'last_name',
            'email',
        )