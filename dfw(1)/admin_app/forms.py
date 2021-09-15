from django.forms import fields, ModelForm
from auth_app import models
from auth_app.models import BookUser
from auth_app.forms import BookUserEditForm
from mainapp.models import BookCategory, Books


class BookUserAdminEditForm(BookUserEditForm):
    class Meta:
        model = BookUser
        fields = '__all__'


class CatEditForm(ModelForm):
    class Meta:
        model = BookCategory
        fields = '__all__'


class BookEditForm(ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

