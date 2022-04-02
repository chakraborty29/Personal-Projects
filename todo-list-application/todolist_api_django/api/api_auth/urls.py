from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views

# router = SimpleRouter()
# router.register('users', views.UserViewset, basename="users")
# router.register('firebase-athlete-user-created', firebase_athlete_user_created, basename='firebase-athlete-ser-created')

urlpatterns = [
    path('auth/firebase-user-created/', views.firebase_user_created),
    path('auth/check-duplicate-username/', views.check_duplicate_username),
    # path('auth/', include(router.urls)),
]