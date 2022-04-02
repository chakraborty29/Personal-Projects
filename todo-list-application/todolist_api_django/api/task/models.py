import uuid
from django.db import models
from api_auth.models import User
# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    TODO = 'todo'
    DONE = 'done'

    STAUS_CHOICES = (
        (TODO, 'Todo'),
        (DONE, 'Done')
    )

    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STAUS_CHOICES , default=TODO)