from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from appel.defaults import DEFAULT_TEACHER_EMAIL, DEFAULT_TEACHER_PASSWORD, DEFAULT_TEACHER_USERNAME


class Command(BaseCommand):
    help = 'Create or update default user with specified credentials'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=DEFAULT_TEACHER_USERNAME,
            defaults={
                'email': DEFAULT_TEACHER_EMAIL,
                'is_staff': False,
            },
        )
        user.email = DEFAULT_TEACHER_EMAIL
        user.is_staff = False
        user.set_password(DEFAULT_TEACHER_PASSWORD)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully {"created" if created else "updated"} user: {user.username}\n'
                f'Password: {DEFAULT_TEACHER_PASSWORD}\n'
                f'Email: {user.email}'
            )
        )
