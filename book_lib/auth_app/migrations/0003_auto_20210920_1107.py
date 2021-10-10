# Generated by Django 3.2.4 on 2021-09-20 07:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_auto_20210916_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 22, 7, 6, 59, 855119, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bookuser',
            name='age',
            field=models.PositiveIntegerField(default=99, verbose_name='Возраст'),
        ),
        migrations.CreateModel(
            name='BookUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(blank=True, max_length=128, verbose_name='Теги')),
                ('aboutme', models.TextField(blank=True, max_length=1024, verbose_name='О себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=1, verbose_name='пол')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
