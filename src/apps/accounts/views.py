from django.shortcuts import render
from django.db import IntegrityError
from django_base.utils import send_email
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django_base.settings import SITE_NAME
from .models import CustomUser
from .forms import LoginForm, RegForm, ResetPasswordForm, SetPasswordForm


def auth_login(request):
    '''
    Авторизация пользователя
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Если не поставлена галочка "запомнить меня"
                    if not remember_me:
                        request.session.set_expiry(0)

                    return HttpResponseRedirect(reverse('index'))
            else:
                return render(
                    request,
                    "error.html",
                    {
                        "error_title": _('Ошибка авторизации!'),
                        "error_description": _('Вероятно, вы ввели некорректное имя пользователя и/или пароль.')
                    }
                )
    else:
        return HttpResponseNotAllowed()

    return render(request, 'login.html', {'form': form})


def auth_logout(request):
    '''
    Выход пользователя
    '''
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


def registration(request):
    '''
    Регистрация нового пользователя
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'GET':
        form = RegForm()
    elif request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            username = '%s' % form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Check username
            try:
                user = CustomUser.objects.get(username=username)

                return render(
                    request,
                    "error.html",
                    {
                        "error_title": _('Ошибка регистрации!'),
                        "error_description": _('Пользователь с именем \'%s\' уже существует!' % username)
                    }
                )
            except ObjectDoesNotExist:
                pass

            # Check e-mail
            try:
                user = CustomUser.objects.get(email=email)

                return render(
                    request,
                    "error.html",
                    {
                        "error_title": _('Ошибка регистрации!'),
                        "error_description": _('Пользовательс с e-mail \'%s\' уже существует!' % email)
                    }
                )
            except ObjectDoesNotExist:
                pass

            # Check password
            if password1 == password2:
                user = CustomUser.objects.create_user(username, email, password1)

                subject = _('Подтверждение регистрации')
                link = SITE_NAME+'/accounts/activate/%s' % user.key

                html = render_to_string(
                    'mail/registration_confirm.html',
                    {
                        'subject': subject,
                        'link': link,
                        'host': SITE_NAME
                    }
                )

                if not send_email(subject, html, email):
                    return render(
                        request,
                        "error.html",
                        {
                            "error_title": _('Ошибка регистрации!'),
                            "error_description": _('''
                                При отправки регистрационного письма возникла ошибка.
                                Пожалуйста, попробуйье повторить позднее!
                            ''')
                        }
                    )

                return HttpResponseRedirect(reverse('accounts:thanks'))
            else:
                return render(
                    request,
                    "error.html",
                    {
                        "error_title": _('Ошибка регистрации!'),
                        "error_description": _('Пароли не совпадают!')
                    }
                )
    else:
        return HttpResponseNotAllowed()

    return render(request, 'registration.html', {'form': form})


def activate(request, key):
    '''
    Проверка рег.ссылки и активирование учетной записи пользователя
    '''
    if request.user.is_active:
        return HttpResponseRedirect(reverse('index'))

    try:
        user = CustomUser.objects.get(key=key)
        user.is_active = True
        user.key = user._gen_hash()
        user.save()
        login(request, user)
    except IntegrityError:
        return render(
            request,
            "error.html",
            {
                "error_title": _('Ошибка активации!'),
                "error_description": _('Невозможно обновить данные пользователя!')
            }
        )
    except ObjectDoesNotExist:
        return render(
            request,
            "error.html",
            {
                "error_title": _('Ошибка активации!'),
                "error_description": _('Попытка регистрации по несуществующему или устаревшему ключу!')
            }
        )

    return render(request, "activated.html")


def set_password(request, key):
    '''
    Задание нового пароля пользователя
    '''
    if request.user.is_active:
        return HttpResponseRedirect(reverse('index'))
    try:
        user = CustomUser.objects.get(key=key)
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return HttpResponseRedirect(reverse('accounts:login'))
                else:
                    return HttpResponseRedirect(reverse('accaunts:set_password', kwargs={'key': key}))
        else:
            form = SetPasswordForm()
        return render(request, 'set_password.html', {'form': form, 'key': key})
    except ObjectDoesNotExist:
        return render(
            request,
            "error.html",
            {
                "error_title": _('Ошибка восстановления!'),
                "error_description": _('Попытка восстановления пароля для несуществующего пользователя!')
            }
        )
    return HttpResponseRedirect(reverse('accounts:login'))


def reset_password(request):
    '''
    Сброс старого пароля пользователя
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                subject = _('Создание нового пароля для BlankDJP')
                link = '127.0.0.1:8000/accounts/set_new_password/%s' % user.key
                html = render_to_string('mail/reset_password_confirm.html', {
                    'subject': subject, 'link': link,
                })
                sending_result = send_email(subject, html, email)

                if not sending_result:
                    return render(
                        request,
                        "error.html",
                        {
                            "error_title": _('Ошибка изменения пароля!'),
                            "error_description": _('''
                                При отправки регистрационного письма возникла ошибка.
                                Пожалуйста, попробуйье повторить позднее!
                            ''')
                        }
                    )

                return HttpResponse(_('На указзанный e-mail были отправлены Ваши пользовательские данные.'))
            except ObjectDoesNotExist:
                return render(
                    request,
                    "error.html",
                    {
                        "error_title": _('Ошибка изменения пароля!'),
                        "error_description": _('Пользователь с email \'%s\' не зарегистрирован!' % email)
                    }
                )
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


def thanks(request):
    '''
    Страница сообщения, что аккаунт зарегистрирован, письмо отправлено
    '''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'thanks.html')


def show_profile(request):
    '''
    Страница обновление профиля пользователя
    '''
    return render(request, 'profile.html')
