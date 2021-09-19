from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

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

