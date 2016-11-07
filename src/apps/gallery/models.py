from django.db import models
from django_base.db import ImgThumbsField
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class GalleryManager(models.Manager):
    def get_queryset(self):
        return super(GalleryManager, self).get_queryset().filter(is_public=True)


class Gallery(models.Model):
    title = models.CharField('Название галереи', max_length=128)
    slug = models.SlugField(
        'Транслитерация',
        unique=True,
        help_text='Название галереи (заполняется автоматически)'
    )
    desc = models.TextField(
        'Описание галереи',
        validators=[MaxLengthValidator(256)],
        blank=True
    )
    is_public = models.BooleanField('Опубликовано', default=True)
    pub_date = models.DateTimeField('Дата и врем публикации галереи', blank=True)

    objects = models.Manager()
    gallery_objects = GalleryManager()

    class Meta:
        db_table = 'galleries'
        verbose_name = 'галерею'
        verbose_name_plural = 'Галереи'

    def save(self, *args, **kwargs):
        if not self.pub_date and self.is_public:
            self.pub_date = timezone.now()
        super(Gallery, self).save(*args, **kwargs)

    def __str__(self):
        return 'Название выбранной галереи: \'%s\'' % self.title


class Image(models.Model):
    img = ImgThumbsField(
        'Изображение',
        sizes={
            '255x180': ('sm', 80),
            '256x256': ('min', 80),
            '1024x768': ('mid', 80),
            '1280x1024': ('full', 80),
        },
        upload_to='gallery/'
    )
    sign = models.CharField(
        'Подпись к изображением',
        max_length=128,
        blank=True,
        help_text='Текст, который будет отображен как подпись к изображению'
    )
    position = models.PositiveSmallIntegerField(
        'Порядок следования',
        choices=[(x, x) for x in range(1, 101)],
        default=1
    )
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея')

    class Meta:
        db_table = 'gallery_images'
        verbose_name = 'файл изображения'
        verbose_name_plural = 'Изображения'
        ordering = ['position']

    def __str__(self):
        return '%s' % self.sign if self.sign else self.img.url
