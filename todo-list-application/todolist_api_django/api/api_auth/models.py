from django.db import models

from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Firebase Identifier
    firebase_id = models.CharField(max_length=255, blank=False, null=False, unique=True)

    # Admin Roles
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # User data
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, default=None, null=True)
    last_name = models.CharField(max_length=255, blank=True, default=None, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)