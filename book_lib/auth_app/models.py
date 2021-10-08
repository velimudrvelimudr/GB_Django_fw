from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class BookUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', verbose_name='Аватар', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=99)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        """ Проверяет, действителен ли код активации. """

        return False if now() <= self.activation_key_expires else True

    def __str__(self) -> str:
        return super().__str__()

    def user_count(self):
        """ Возвращает количество книг в библиотеке пользователя.  """

        return len(self.perslib.all())


class BookUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(
        BookUser, 
        unique=True, 
        null=False, 
        db_index=True, 
        on_delete=models.CASCADE
    )

    tags = models.CharField(
        verbose_name='Теги',
        max_length=128,
        blank=True
    )

    aboutme = models.TextField(
        verbose_name='О себе',
        max_length=1024,
        blank=True
    )
    
    gender = models.CharField(
        verbose_name='пол',
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )

    @receiver(post_save, sender=BookUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            BookUserProfile.objects.create(user=instance)


    @receiver(post_save, sender=BookUser)
    def save_user_brofile(sender, instance, **kwargs):
        instance.bookuserprofile.save()

