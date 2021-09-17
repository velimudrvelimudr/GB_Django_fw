from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from csv import DictReader
from mainapp.models import BookCategory, Books
from userlibrapp.models import PersonLib


# Create your views here.

def main(request):
    """ Отображает главную страницу. 
    На странице выводится меню категорий.  """

    content = {
        'cat_menu':BookCategory.objects.order_by('name'),
    }

    return render(request, 'mainapp/index.html', context=content)


def catalog(request, pk=None, num_page=1):
    """ Отображение каталога. Если указан ID категории, то только книг из этой категории. """

    if pk:
        book_list = Books.objects.all().filter(cat_fk=pk)
        topic = BookCategory.objects.get(pk=pk)
    else:
        book_list = Books.objects.all()
        topic = None

    cat_menu = BookCategory.objects.all().order_by('name')

    paginator = Paginator(book_list, 10)
    try:
        books_paginator = paginator.page(num_page)
    except PageNotAnInteger:
        books_paginator = paginator.page(1)
    except EmptyPage:
        books_paginator = paginator.page(paginator.num_pages)

    content = {
        'books':books_paginator,
        'topic': topic,
        'cat_menu':cat_menu,
    }

    return render(request, 'mainapp/catalog.html', context=content)


def show_book_info(request, book_id):
    """ Вывод информации о книге. """

    book = Books.objects.get(id=book_id)

    if request.user.is_authenticated:
        user_book = request.user.perslib.filter(book__id=book_id, user=request.user)
        if len(user_book) == 1:
            url_view = 'libr:rm_book'
            url_id = user_book.first().id
            url_text = 'Удалить из библиотеки'
        else:
            url_view = 'libr:add_book'
            url_id = book_id
            url_text = 'Добавить в библиотеку'
    else:
        url_text = None
        url_id = None
        url_view = None

    book_info = Books.objects.get(id=book_id)
    book_count = book.book_count # В подробных данных о книге покажем, сколько читателей её себе добавили.

    context = {
        'bookinfo':book_info,
        'book_count':book_count,
        'url_data':(url_view, url_id, url_text),
    }
    return render(request, 'mainapp/book.html', context=context)


def contacts(request):
    """ Страница контактов.  """

    return render(request, 'mainapp/contacts.html')

def test(request):
    return render(request, 'mainapp/test.html', {'title':'Тестовая страница'})
