from django.urls import path
import auth_app.views as     authapp

app_name = 'auth_app'


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('profile/', authapp.profile, name='profile'),
    path('edit/', authapp.edit, name='edit'),
    path('register/', authapp.register, name='register'),
]

