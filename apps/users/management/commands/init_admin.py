from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create or update default admin superuser (admin / 123)'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = '123'
        email = 'admin@example.com'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'full_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        if hasattr(user, 'role'):
            user.role = 'admin'
        if not user.full_name:
            user.full_name = 'Administrator'
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' successfully created with password '{password}'."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists. Password updated to '{password}'."))
