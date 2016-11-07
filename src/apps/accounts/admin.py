from django import forms
from .models import CustomUser
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.templatetags.static import static
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (
            _('Аккаунт'),
            {
                'fields': (('username', 'email'), 'avatar', 'password', 'key')
            }
        ),
        (
            _('Личная информация'),
            {
                'fields': (('fname', 'lname'), 'info')
            }
        ),
        (
            _('Права доступа'),
            {
                'fields': (
                    ('is_admin', 'is_superuser', 'is_active', 'is_approved'),
                )
            }
        ),
    )

    add_fieldsets = (
        (
            _('Новый пользователь'),
            {
                'classes': ('wide',),
                'fields': (('username', 'email'), ('password1', 'password2'))
            }
        ),
    )

    list_display = ('thumbnail_avatar', 'username', 'email', 'key', 'is_approved')
    list_display_links = ('thumbnail_avatar', 'username')
    list_filter = ('is_admin', 'is_superuser', 'is_active', 'is_approved')
    search_fields = ('username', 'email', 'fname', 'lname', 'info', 'key')
    ordering = ('username', 'email', 'fname', 'lname')
    filter_horizontal = ()

    def thumbnail_avatar(self, obj):
        if obj.avatar:
            return format_html(
                "<img src='%s' alt='%s-avatar' />" % (
                    obj.avatar.url_mid, obj.username
                )
            )
        else:
            return format_html(
                "<img src='%s' width='128' height='128' alt='avatar' />" % static(
                    'app/img/avatar.svg'
                )
            )
    thumbnail_avatar.short_description = _('Аватар')
    thumbnail_avatar.allow_tags = True


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
