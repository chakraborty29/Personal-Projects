from django.shortcuts import render
from django.http import response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer
from .utils import app
# Create your views here.

# Set up Firebase Admin
default_app = app()


@api_view(['POST'])
def firebase_user_created(request):
    data = request.data

    first_name = data['first_name']
    last_name = data['last_name']
    uid = data['uid']
    username = data['username']


    if not (first_name and last_name and uid and username):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.filter(firebase_id=uid).update(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def check_duplicate_username(request):
    username = request.GET.get('username')

    try:
        user = User.objects.get(username=username)
        if user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)  
    except User.DoesNotExist:
        return Response(status=status.HTTP_200_OK)


# DO NOT DEPLY WITH THIS UNCOMMENTED THIS IS FOR TEST PURPOSES ONLY
# class UserViewset(viewsets.ModelViewSet):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         return User.objects.all() 