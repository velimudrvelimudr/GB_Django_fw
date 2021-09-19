from django.shortcuts import render, HttpResponseRedirect
from auth_app.forms import BookLoginUserForm, BookUserEditForm, BookUserRegisterForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from userlibrapp.models import PersonLib
from django.core.mail import send_mail
from django.conf import settings
from auth_app.models import BookUser

# Create your views here.

def login(request):
    """ Страница авторизации.  """

    title = 'Вход'
    login_form = BookLoginUserForm(data=request.POST)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form':login_form,
    }

    return render(request, 'auth_app/login.html', context=content)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def profile(request):
    """ Просмотр профиля аутентифицированного пользователя. """

    title = 'Профиль пользователя'

    context = {
        'title':title,
    }

    return render(request, 'auth_app/profile_view.html', context=context)


@login_required
def edit(request):
    """ Редактирование профиля пользователя.  """

    title = 'Изменить профиль пользователя'

    if request.method == 'POST':
        edit_form = BookUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        edit_form = BookUserEditForm(instance=request.user)

    context = {
        'title':title,
        'form': edit_form,
        'id_view':'edit',
    }

    return render(request, 'auth_app/profile_editor.html', context=context)


def register(request):
    """ Регистрация нового пользователя """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth:profile')) # Аутентифицированным пользователям здесь делать нечего.

    title = 'Регистрация нового пользователя'
    
    if request.method == 'POST':
        reg_form = BookUserRegisterForm(request.POST, request.FILES)
        if reg_form.is_valid():
            user = reg_form.save(commit=True)
            if send_verify_mail(user=user):
                print('Сообщение с активационным кодом успешно отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        reg_form = BookUserRegisterForm

    context = {
        'title':title,
        'form':reg_form,
        'id_view':'registr',
        'user_count': None,
    }

    return render(request, 'auth_app/profile_editor.html', context)


def send_verify_mail(user):
    """ Отправка пользователю письма с активационным кодом. """

    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учётной записи пользователя {user.username}'
    msg = f'Для подтверждения учётной записи на портале {settings.DOMAIN_NAME} перейдите по ссылке\n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, msg, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    """ Верификация пользователя """

    try:
        user = BookUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'auth_app/verify.html')
        else:
            print(f'Ошибка активации пользователя {user.username}')
            return render(request, 'auth_app/verify.html')
    except Exception as e:
        print(f'Ошибка активации пользователя: {e.args}')
        return HttpResponseRedirect(reverse('main'))

