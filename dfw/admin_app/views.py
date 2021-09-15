from django.http import request
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import DeleteView
from auth_app.models import BookUser
from auth_app.forms import BookUserRegisterForm
from mainapp.models import BookCategory, Books
from admin_app.forms import BookUserAdminEditForm, CatEditForm, BookEditForm


# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    """ Список пользователей. """

    users = BookUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    title = 'Список пользователей'

    context ={
        'users': users,
        'title': title,
    }

    return render(request, 'admin_app/users.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_info(request, pk):
    """ Информация о пользователе. """

    user = get_object_or_404(BookUser, pk=pk)
    title = 'Данные пользователя.'

    context = {
        'user': user,
        'title': title,
    }

    return render(request, 'admin_app/user_info.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    """ Создание пользователя админом. """

    title = 'Создание нового пользователя администратором'

    if request.method == 'POST':
        user_form = BookUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid:
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = BookUserRegisterForm()

    context = {
        'title': title,
        'edit_form': user_form,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_change(request, pk):
    """ Редактирование профиля пользователя админом. """

    title = 'Редактирование профиля пользователя администратором'

    change_user = get_object_or_404(BookUser, pk=pk)

    if request.method == 'POST':
        change_form = BookUserAdminEditForm(request.POST, request.FILES, instance=change_user)
        if change_form.is_valid:
            change_form.save()
            return HttpResponseRedirect(reverse('admin:user_info', args=[change_user.pk]))
    else:
        change_form = BookUserAdminEditForm(instance=change_user)

    context = {
        'title': title,
        'edit_form': change_form,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    """ Удаление пользователя. """

    title = 'Удаление пользователя'
    user_to_delete = get_object_or_404(BookUser, pk=pk)

    if request.method == 'POST':
        user_to_delete.delete()
        return HttpResponseRedirect(reverse('admin:users'))

    context = {
        'title': title,
        'user_to_delete': user_to_delete,
    }
    return render(request, 'admin_app/delete_user.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def cats(request):
    """ Список категорий.  """

    cats = BookCategory.objects.all().order_by('name')
    title = 'Список категорий'

    context = {
        'cats': cats,
        'title': title,
    }

    return render(request, 'admin_app/cats.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def change_cat(request, pk):
    """ Изменение категории. """

    title = 'Редактирование категории'
    cat = get_object_or_404(BookCategory, pk=pk)

    if request.method == 'POST':
        edit_cat = CatEditForm(request.POST, instance=cat)
        if edit_cat.is_valid:
            edit_cat.save()
            return HttpResponseRedirect(reverse('admin:cats'))
    else:
        edit_cat = CatEditForm(instance=cat)
    
    context = {
        'title': title,
        'cat': cat,
        'edit_form': edit_cat,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def cat_info(request, pk):
    """ Информация о категории. """

    cat = get_object_or_404(BookCategory, pk=pk)
    title = 'Информация о категории'

    context = {
        'cat': cat,
        'title': title
    }

    return render(request, 'admin_app/cat_info.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def cat_add(request):
    """ Добавление категории """

    title = 'Добавление новой категории'

    if request.method == 'POST':
        add_form = CatEditForm(request.POST)
        if add_form.is_valid:
            add_form.save()
            return HttpResponseRedirect(reverse('admin:cats'))
    else:
        add_form = CatEditForm()

    context = {
        'title': title,
        'edit_form': add_form,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def cat_delete(request, pk):
    """ Удаление категории """

    title = 'Удалить категорию'
    cat_to_delete = get_object_or_404(BookCategory, pk=pk)

    if request.method == 'POST':
        cat_to_delete.delete()
        return HttpResponseRedirect(reverse('admin:cats'))
        
    context = {
        'title': title,
        'cat_to_delete': cat_to_delete,
    }

    return render(request, 'admin_app/delete_cat.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def books(request, cat=None):
    """ Список книг. """

    title = 'Список книг'
    cat_menu = BookCategory.objects.all().order_by('name')

    if cat:
        books = Books.objects.filter(cat_fk=cat).order_by('author', 'name')
        cat_name = get_object_or_404(BookCategory, pk=cat).name
    else:
        books = Books.objects.all().order_by('author', 'name')
        cat_name = None

    context = {
        'books': books,
        'title': title,
        'cat_name': cat_name,
        'cat_menu': cat_menu,
    }

    return render(request, 'admin_app/books.html', context=context)


class BooksLV(ListView):
    model = Books
    template_name = 'admin_app/books.html'


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def  dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):

        if self.kwargs.get('cat'):
            return super().get_queryset().filter(cat_fk=self.kwargs['cat']).order_by('name')

        return super().get_queryset().order_by('name')


    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список книг'
        context['cat_menu'] = BookCategory.objects.all().order_by('name')

        if self.kwargs.get('cat'):
            context['cat_name'] = get_object_or_404(BookCategory, pk=self.kwargs['cat']).name
        else:
            context['cat_name'] = None

        return context


@user_passes_test(lambda u: u.is_superuser)
def book_info(request, pk):
    """ Информация о книге. """

    title = 'Информация о книге'
    book = get_object_or_404(Books, pk=pk)

    context = {
        'title': title,
        'book': book,
    }

    return render(request, 'admin_app/book_info.html', context=context)


class BookDetail(DetailView):
    model = Books
    template_name = 'admin_app/book_info.html'
    context_object_name = 'book'


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def  dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Информация о книге'

        return context


@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    """ Добавление книги в библиотеку.  """

    title = 'Добавление книги'

    if request.method == 'POST':
        edit_form = BookEditForm(request.POST, request.FILES)
        if edit_form.is_valid:
            nb = edit_form.save()
            return HttpResponseRedirect(reverse('admin:book_info', args=[nb.pk]))
    else:
        edit_form = BookEditForm()

    context = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


class BookAdd(CreateView):
    model = Books
    template_name = 'admin_app/change_obj.html'
    fields = '__all__'
    extra_context = {'title': 'Добавить книгу'}

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('admin:book_info', args=[self.object.pk])


@user_passes_test(lambda u: u.is_superuser)
def change_book(request, pk):
    """ Редактирование данных о книге. """

    title = 'Отредактировать данные книги'
    book = get_object_or_404(Books, pk=pk)

    if request.method == 'POST':
        edit_form = BookEditForm(request.POST, request.FILES, instance=book)
        if edit_form.is_valid:
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:book_info', args=[pk]))
    else:
        edit_form = BookEditForm(instance=book)

    context = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'admin_app/change_obj.html', context=context)


class BookChange(UpdateView):
    model = Books
    template_name = 'admin_app/change_obj.html'
    fields = '__all__'
    extra_context = {'title': 'Изменить данные книги'}


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('admin:book_info', args=[self.get_object().pk])


@user_passes_test(lambda u: u.is_superuser)
def del_book(request, pk):
    """ Удаление книги. """

    title = 'Удалить книгу'
    book_to_delete = get_object_or_404(Books, pk=pk)

    if request.method == 'POST':
        book_to_delete.delete()
        return HttpResponseRedirect(reverse('admin:books', args=[book_to_delete.cat_fk.pk]))
    else:
        context = {
            'title': title,
            'object': book_to_delete,
        }

        return render(request, 'admin_app/delete_book.html', context=context)


class BookDelete(DeleteView):
    model = Books
    template_name = 'admin_app/delete_book.html'
    success_url = reverse_lazy('admin:books')
    extra_context = {'title': 'Удалить книгу'}


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def  dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.del_book = self.get_object()
        self.del_book.delete()
        return HttpResponseRedirect(self.get_success_url())