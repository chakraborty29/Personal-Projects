import os
from .utils import app
from .models import User
from django.utils import timezone
from firebase_admin import auth
from rest_framework import authentication

from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken



default_app = app()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")
            pass

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        
        try:
            email = decoded_token.get("firebase").get('identities').get('email')[0]
        except Exception:
            raise FirebaseError()

        try:
            user = User.objects.get(firebase_id=uid)
        except User.DoesNotExist:
            user = User.objects.create(firebase_id=uid, email=email)

        # user.profile.last_activity = timezone.localtime()

        return (user, None)