from django import forms
from django.utils.translation import ugettext_lazy as _


class ProfileForm(forms.Form):
    avatar = forms.FileField(required=False)
    username = forms.CharField(min_length=2, max_length=64, required=True)
    email = forms.EmailField(min_length=6, max_length=32, required=True)
    fname = forms.CharField(min_length=2, max_length=64, required=False)
    lname = forms.CharField(min_length=2, max_length=64, required=False)
    info = forms.CharField(min_length=2, max_length=512, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Имя пользователя'), min_length=2, max_length=64, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_('Пароль'), min_length=6, max_length=32, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    remember_me = forms.BooleanField(
        label=_('Запомнить меня'),
        widget=forms.CheckboxInput(),
        required=False,
        initial=True
    )


class RegForm(forms.Form):
    username = forms.CharField(
        label=_('Имя пользователя'), min_length=3, max_length=32, required=True,
        widget=forms.TextInput(attrs={'class': 'col-md-10 form-control'})
    )
    email = forms.EmailField(
        label=_('E-mail'), min_length=6, max_length=32, required=True,
        widget=forms.TextInput(attrs={'class': 'col-md-10 form-control'})
    )
    password1 = forms.CharField(
        label=_('Пароль'), min_length=6, max_length=32, required=True,
        widget=forms.PasswordInput(attrs={'class': 'col-md-10 form-control'}),
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'), min_length=6, max_length=32, required=True,
        widget=forms.PasswordInput(attrs={'class': 'col-md-10 form-control'}),
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_('E-mail'), min_length=6, max_length=32, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_('Пароль'), min_length=6, max_length=32, required=True,
        widget=forms.PasswordInput(attrs={'class': 'col-md-10 form-control'}),
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'), min_length=6, max_length=32, required=True,
        widget=forms.PasswordInput(attrs={'class': 'col-md-10 form-control'}),
    )
