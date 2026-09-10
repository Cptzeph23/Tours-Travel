
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create/update a superuser from environment variables"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not password:
            self.stdout.write("DJANGO_SUPERUSER_PASSWORD is not set; skipping superuser creation.")
            return

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser {username}"))
        else:
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Updated superuser {username}"))