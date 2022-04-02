from django.shortcuts import render

from .models import Task
from .serializers import TaskSerialzier

from rest_framework import viewsets
# from rest_framework.authentication import BasicAuthentication
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerialzier
    queryset = Task.objects.all()

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user
        )

