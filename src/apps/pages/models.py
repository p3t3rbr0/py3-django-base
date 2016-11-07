from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MaxLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django_base.utils import get_filenames


class PageManager(models.Manager):
    def get_queryset(self):
        return super(PageManager, self).get_queryset().filter(is_public=True)


class Page(models.Model):
    mdesc = models.TextField(
        _('Описание страницы'),
        validators=[MaxLengthValidator(200)],
        blank=True,
        help_text=_('Краткое описание страницы для поисковых систем (не более 200 смволов)')
    )
    mkeys = models.TextField(
        _('Ключевые слова'),
        validators=[MaxLengthValidator(250)],
        blank=True,
        help_text=_('Перечень поисковых фраз через запятую (для поисковых систем)')
    )
    mtitle = models.CharField(
        _('Заголовок'),
        max_length=80,
        blank=True,
        help_text=_('Заголовок для данной страницы (название вкладки в браузере)')
    )
    title = models.CharField(
        _('Заголовок страницы'),
        max_length=128,
        blank=True
    )
    body = RichTextField(_('Основной контент'), blank=True)
    template = models.CharField(
        _('Шаблон'),
        choices=get_filenames('apps/pages/templates/content_pages', 'html'),
        max_length=32,
        default='default.html'
    )
    gallery = models.ForeignKey(
        'gallery.Gallery',
        verbose_name=_('Галерея'),
        blank=True,
        null=True,
        help_text=_('Отображать на данной странице указанную галерею')
    )
    last_update = models.DateTimeField(_('Последнее обновление'))
    is_public = models.BooleanField(_('Опубликовано'), default=True)
    is_index = models.BooleanField(_('Главная'), default=False)
    in_footer = models.BooleanField(_('Отображать в футере'), default=False)

    objects = models.Manager()
    page_objects = PageManager()

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(Page, self).save(*args, **kwargs)

    class Meta:
        db_table = 'pages'
        verbose_name = _('страницу')
        verbose_name_plural = _('Страницы')
        ordering = ['last_update', 'title']

    def __str__(self):
        return self.title


class Menu(MPTTModel):
    parent = TreeForeignKey(
        'self',
        verbose_name='Родитель',
        null=True,
        blank=True,
        help_text=_('Родительский пункт меню')
    )
    title = models.CharField(
        _('Название пункта'),
        max_length=128,
        blank=True,
        help_text=_('Название пункта меню')
    )
    slug = models.SlugField(
        _('Транслит названия'),
        unique=True,
        blank=True,
        max_length=128,
        help_text=_('Часть URL (заполняется автоматически)')
    )
    position = models.PositiveSmallIntegerField(
        _('Порядок следования'),
        choices=[(x, x) for x in range(1, 101)],
        blank=True,
        help_text=_('Порядок следования данного пункта меню относительно других пунктов')
    )
    external_link = models.URLField(
        _('Внешняя ссылка'),
        max_length=128,
        blank=True,
        help_text=_('Ссылка на внешний источник')
    )
    page = models.ForeignKey(
        Page,
        verbose_name=_('Страница'),
        blank=True,
        null=True,
        help_text=_('Прикрепить страницу к данному пункту меню')
    )
    is_visible = models.BooleanField('Отображать в меню', default=True)
    is_separate = models.BooleanField('Вставить разделитель', default=False)

    def inc_position(self):
        self.position += 1
        self.save()

    def dec_position(self):
        if self.position > 1:
            self.position -= 1
            self.save()

    def save(self, *args, **kwargs):
        if not self.position:
            pos = 1
            if self.parent:
                try:
                    queryset = Menu.objects.filter(parent=self.parent)
                    pos = queryset.latest('position').position + 1
                except Exception:
                    pass
            else:
                try:
                    pos = Menu.objects.latest('position').position + 1
                except Menu.DoesNotExist:
                    pass
            self.position = pos

        # Set menu title and slug
        if self.page and not self.title:
            self.title = self.page.title
            if not self.slug:
                self.slug = slugify(self.page.title)

        Menu.objects.rebuild()  # Hack: Чтобы корректно упорядочивались по position
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        db_table = 'menus'
        verbose_name = _('пункт меню')
        verbose_name_plural = _('Меню')
        ordering = ['position']

    class MPTTMeta:
        level_attr = 'mptt_level'
        parent_attr = 'parent'
        order_insertion_by = ['position']

    def get_absolute_url(self):
        return reverse('pages:show_page', args=[self.slug])

    def __str__(self):
        return self.title
