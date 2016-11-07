from django.db import models
from django_base.db import ImgThumbsField
from django.core.urlresolvers import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    '''
    Модель новостных категорий
    '''
    title = models.CharField(_('Название категории'), max_length=64, unique=True)
    slug = models.SlugField(
        _('Транслит названия'),
        max_length=64,
        unique=True,
        help_text=_('Транслитерация названия названия категориий. Является частью URL. Заполняется автоматически.')
    )

    class Meta:
        db_table = 'categories'
        verbose_name = _('категорию')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class Tag(models.Model):
    '''
    Модель тегов новостей
    '''
    title = models.CharField(_('Название тега'), max_length=32, unique=True)
    slug = models.SlugField(
        _('Транслит названия'),
        max_length=32,
        unique=True,
        help_text=_('Транслитерация названия тега. Является частью URL. Заполняется автоматически.')
    )

    class Meta:
        db_table = 'tags'
        verbose_name = _('тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.title


class NewsManager(models.Manager):
    '''
    Менеджер модлеи новостей. Осуществляет первичную фильтрацию только опубликованных новостей.
    '''
    def get_queryset(self):
        return super(NewsManager, self).get_queryset().filter(is_public=True)


class News(models.Model):
    '''
    Модель новостей
    '''
    title = models.CharField(
        _('Заголовок новости'),
        max_length=150,
        help_text=_('Не более 150 знаков')
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        related_name='category',
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='tags', blank=True)
    cover = ImgThumbsField(
        _('Обложка'),
        upload_to='news/',
        sizes={
            '64x64': ('xs', 80),
            '128x128': ('sm', 80),
            '256x256': ('min', 80),
            '1024x768': ('mid', 80),
            '1280x1024': ('full', 80),
        },
        help_text=_('Главное изображение новости')
    )
    teaser = models.TextField(
        _('Краткое содержание новости'),
        validators=[MaxLengthValidator(500)],
        help_text=_('Краткая аннотация новости. Текст не более 500 знаков.')
    )
    body = RichTextUploadingField(
        _('Основной контент'),
        blank=True,
        help_text=_('Основное содержимое новости')
    )
    pub_date = models.DateTimeField(_('Дата и время'))
    author = models.ForeignKey('accounts.CustomUser', verbose_name=_('Автор новости'))
    gallery = models.ForeignKey(
        'gallery.Gallery',
        verbose_name=_('Галерея'),
        blank=True,
        null=True,
        help_text=_('Отображать на данной странице указанную галерею')
    )
    is_public = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Опубликовать новость после сохранения')
    )

    objects = models.Manager()
    news_objects = NewsManager()

    class Meta:
        db_table = 'news'
        verbose_name = _('новость')
        verbose_name_plural = _('Новости')
        ordering = ['-pub_date']

    def __str__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.pk])
