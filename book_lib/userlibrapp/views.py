from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from mainapp.models import Books
from userlibrapp.models import PersonLib

# Create your views here.

@login_required
def perslib(request):
    """ Просмотр библиотеки пользователя. """

    title = 'Библиотека пользователя'
    user_books = request.user.perslib.all().order_by('add_datetime')

    context = {
        'title':title,
        'user_books':user_books,
    }

    return render(request, 'userlibrapp/userlibr.html', context=context)


@login_required
def add_book(request, pk):
    """ Добавление книги в библиотеку. """

    book = get_object_or_404(Books, pk=pk)

    user_book = request.user.perslib.filter(book=book).first()

    if not user_book:
        user_book = PersonLib(user=request.user, book=book)
        user_book.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def rm_book(request, pk):
    """ Удаление книги из библиотеки.  """

    user_book = get_object_or_404(PersonLib, pk=pk, user=request.user)

    if user_book:
        user_book.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

