from django.urls.conf import path
import admin_app.views as my_admin

app_name = 'admin_app'

urlpatterns = [
    path('', my_admin.users),
    path('users/', my_admin.users, name='users'),
    path('user_info/<int:pk>/', my_admin.user_info, name='user_info'),
    path('new_user/', my_admin.user_create, name='new_user'),
    path('change_user/<int:pk>/', my_admin.user_change, name='change_user'),
    path('delete_user/<int:pk>/', my_admin.user_delete, name='user_delete'),
    path('cats/', my_admin.cats, name='cats'),
    path('cat_info/<int:pk>/', my_admin.cat_info, name='cat_info'),
    path('change_cat/<int:pk>/', my_admin.change_cat, name='cat_change'),
    path('add_cat', my_admin.cat_add, name='add_cat'),
    path('cat_delete/<int:pk>/', my_admin.cat_delete, name='cat_delete'),
    # path('books/', my_admin.books, name='books'),
    path('books/', my_admin.BooksLV.as_view(), name='books'),
    # path('books/<int:cat>/', my_admin.books, name='books'),
    path('books/<int:cat>/', my_admin.BooksLV.as_view(), name='books'),
    # path('book_info/<int:pk>/', my_admin.book_info, name='book_info'),
    path('book_info/<int:pk>/', my_admin.BookDetail.as_view(), name='book_info'),
    # path('add_book/', my_admin.add_book, name='add_book'),
    path('add_book/', my_admin.BookAdd.as_view(), name='add_book'),
    # path('change_book/<int:pk>', my_admin.change_book, name='change_book'),
    path('change_book/<int:pk>', my_admin.BookChange.as_view(), name='change_book'),
    path('del_book/<int:pk>/', my_admin.del_book, name='del_book'),
    # path('del_book/<int:pk>/', my_admin.BookDelete.as_view(), name='del_book'),
]
