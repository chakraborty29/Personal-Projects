from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD
ADMIN_EMAIL = settings.ADMIN_EMAIL
ADMIN_FIREBASE_UID = settings.ADMIN_FIREBASE_UID

class Command(BaseCommand):
    help = 'create custom superuser'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=ADMIN_USERNAME)
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
        except User.DoesNotExist:
            try:
                User.objects.create_superuser(
                    username=ADMIN_USERNAME,
                    email=ADMIN_EMAIL,
                    password=ADMIN_PASSWORD,
                    firebase_id=ADMIN_FIREBASE_UID
                )
                self.stdout.write(self.style.SUCCESS("Created superuser!"))
            except Exception as err:
                raise CommandError('Error creating superuser: ' + str(err))
