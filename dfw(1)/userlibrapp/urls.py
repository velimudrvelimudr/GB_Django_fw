from django.urls import path
import userlibrapp.views as userlibrapp

app_name = 'userlibrapp'


urlpatterns = [
    path('', userlibrapp.perslib, name='perslib'),
    path('add/<int:pk>/', userlibrapp.add_book, name='add_book'),
    path('rm/<int:pk>/', userlibrapp.rm_book, name='rm_book'),
]

