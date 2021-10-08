from django.core.management.base import BaseCommand
from auth_app.models import BookUser, BookUserProfile

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = BookUser.objects.all()

        BookUserProfile.objects.all().delete()

        for user in users:
            user_profile = BookUserProfile.objects.create(user=user)
        user_profile.aboutme = f'{user.username} {user.first_name} {user.last_name} возраста {user.age}'
            user_profile.save()
