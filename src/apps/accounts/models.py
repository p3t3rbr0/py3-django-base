from hashlib import md5
from django.db import models
from datetime import datetime
from django_base.db import ImgThumbsField
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError(_('У пользователя должен быть email адрес'))
        if not username:
            raise ValueError(_('У пользователя должно быть имя'))

        user = self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        user = self.create_user(username, email, password=password)
        user.is_admin = user.is_superuser = user.is_active = user.is_approved = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(_('Имя пользователя'), max_length=16, unique=True)
    email = models.EmailField(_('E-mail'), max_length=64, unique=True)
    avatar = ImgThumbsField(
        _('Аватар'),
        sizes={
            '64x64': ('min', 80),
            '128x128': ('mid', 80),
            '512x512': ('full', 80)
        },
        upload_to='accounts/',
        blank=True
    )
    fname = models.CharField(_('Имя'), max_length=50, blank=True)
    lname = models.CharField(_('Фамилия'), max_length=50, blank=True)
    info = models.TextField(_('Дополнительная информация'), validators=[MaxLengthValidator(512)], blank=True)
    key = models.CharField(_('UID'), max_length=64, blank=True, unique=True)
    is_active = models.BooleanField(_('Запись активирована'), default=False)
    is_admin = models.BooleanField(_('Администратор'), default=False)
    is_approved = models.BooleanField(_('Аккаунт подтвержден'), default=False)
    is_superuser = models.BooleanField(_('Привилегированный пользователь'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'accounts'
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self._gen_hash()
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return '%s (%s)' % (self.username, self.email)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return '%s, %s' % (self.name, self.surname)

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def _gen_hash(self):
        return md5(
            str(
                '%s + %s + %s' % (self.username, self.email, str(datetime.utcnow()))
            ).encode('utf-8')
        ).hexdigest()

    @property
    def is_staff(self):
        return self.is_admin
