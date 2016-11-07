from django.contrib import admin
from .models import Gallery, Image


class ImageTaular(admin.TabularInline):
    model = Image
    extra = 0
    sortable_field_name = 'position'


class GalleryAdmin(admin.ModelAdmin):
    fieldsets = [
        (u'Галерея', {
            'fields': [
                ('title', 'slug'), 'desc', 'is_public',
            ],
        }),
    ]

    inlines = [ImageTaular]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'desc', 'pub_date', 'is_public',)
    list_display_links = ('title',)
    list_per_page = 25
    search_fields = ['title', 'slug']
    list_filter = ['is_public', 'pub_date']


admin.site.register(Gallery, GalleryAdmin)
