from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from appel.defaults import DEFAULT_TEACHER_EMAIL, DEFAULT_TEACHER_PASSWORD, DEFAULT_TEACHER_USERNAME


class Command(BaseCommand):
    help = 'Create default user for testing'

    def handle(self, *args, **options):
        username = DEFAULT_TEACHER_USERNAME
        password = DEFAULT_TEACHER_PASSWORD
        email = DEFAULT_TEACHER_EMAIL

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': False},
        )
        user.email = email
        user.is_staff = False
        user.set_password(password)
        user.save()

        message = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Successfully {message} user: {username}'))
