from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BookUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', verbose_name='Аватар', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст')

    def __str__(self) -> str:
        return super().__str__()

    def user_count(self):
        """ Возвращает количество книг в библиотеке пользователя.  """

        return len(self.perslib.all())