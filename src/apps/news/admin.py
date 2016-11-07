from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from .models import Category, Tag, News


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            _('Категория'),
            {'fields': [('title', 'slug')]}
        ),
    ]

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ['title', 'slug']


class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            _('Тег'),
            {'fields': [('title', 'slug')]}
        ),
    ]

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ['title', 'slug']


class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Новость'), {
            'fields': [
                ('title', 'category'), 'cover', 'teaser', 'body', 'tags', 'pub_date', 'gallery', 'is_public'
            ],
        }),
    ]

    radio_fields = {'category': admin.HORIZONTAL}
    raw_id_fields = ('gallery',)
    autocomplete_lookup_fields = {'fk': ['gallery']}
    list_display = ('id', 'img_thumbnail', 'title', 'pub_date', 'author', 'is_public')
    list_display_links = ('id', 'img_thumbnail', 'title')
    list_per_page = 25
    sortable_field_name = 'title'
    search_fields = ['title', 'teaser']
    list_filter = ['is_public', 'pub_date', 'author', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def img_thumbnail(self, obj):
        return format_html(
            "<img src='%s' alt='%s' />" % (obj.cover.url_sm, obj.title)
        )
    img_thumbnail.short_description = _('Превью')
    img_thumbnail.allow_tags = True


admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
