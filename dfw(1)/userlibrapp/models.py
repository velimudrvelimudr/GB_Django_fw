from django.db import models
from django.conf import settings
from mainapp.models import Books

# Create your models here.

class PersonLib(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perslib')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='booklib')
    add_datetime = models.DateTimeField(verbose_name='Добавлена в библиотеку', auto_now_add=True)

