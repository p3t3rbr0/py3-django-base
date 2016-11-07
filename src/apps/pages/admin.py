from django.contrib import admin
from .models import Page, Menu
from django.shortcuts import render, HttpResponse
from mptt.exceptions import InvalidMove
from apps.feincms.admin import tree_editor
from django_base.settings import SITE_NAME
from django.utils.translation import ugettext_lazy as _
from .forms import MenuParentForm


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Метаинформация'), {
            'classes': ('collapse',),
            'fields': [
                'mdesc', 'mkeys', 'mtitle'
            ],
        }),
        (_('Содержимое страницы'), {
            'fields': [
                'title', 'body'
            ],
        }),
        (_('Шаблон и статус'), {
            'fields': [
                ('template', 'is_public', 'is_index')
            ]
        }),
        (_('Галерея'), {
            'fields': [
                'gallery'
            ]
        }),
    ]

    raw_id_fields = ('gallery',)
    autocomplete_lookup_fields = {'fk': ['gallery']}
    list_display = ('id', 'title', 'is_public', 'last_update')
    list_display_links = ('id', 'title')
    list_editable = ('is_public',)
    list_per_page = 100
    sortable_field_name = 'title'
    search_fields = ['title', 'body']
    list_filter = ['last_update', 'is_public', 'is_index']


class MenuAdmin(tree_editor.TreeEditor):
    fieldsets = [
        (_('Пункт меню'), {
            'fields': [
                ('title', 'slug'), 'parent', 'external_link', 'page',
                ('is_visible', 'is_separate')
            ]
        }),
    ]

    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('parent', 'page')
    autocomplete_lookup_fields = {'fk': ['page']}
    list_display = ('title', 'get_link', 'position', 'is_visible', 'is_separate')
    list_display_links = ('title',)
    list_editable = ('position', 'is_visible', 'is_separate')
    list_per_page = 100
    sortable_field_name = 'position'
    search_fields = ['title', 'slug']
    list_filter = ['is_visible']
    actions = ['inc_position_action', 'dec_position_action', 'set_parent_action']

    def get_title(self, obj):
        return '%s (%s)' % (obj.title, obj.slug)
    get_title.short_description = _('Название (ссылка)')

    def get_link(self, obj):
        return obj.external_link if obj.external_link else '%s/pages/%s/' % (SITE_NAME, obj.slug)
    get_link.short_description = _('Ссылка')

    def inc_position_action(self, request, queryset):
        for q in queryset:
            q.inc_position()
        self.message_user(request, _('У выбранных Вами страниц была увеличина позиция на 1'))
    inc_position_action.short_description = _('Увеличить порядок следования у выбранных елементов')

    def dec_position_action(self, request, queryset):
        for q in queryset:
            q.dec_position()
        self.message_user(request, _('У выбранных Вами страниц была уменьшена позиция на 1'))
    dec_position_action.short_description = _('Уменьшить порядок следования у выбранных елементов')

    def set_parent_action(self, request, queryset):
        if 'do_action' in request.POST:
            form = MenuParentForm(request.POST)

            if form.is_valid():
                for q in queryset:
                    try:
                        q.move_to(form.cleaned_data['page'])
                    except InvalidMove as e:
                        return HttpResponse(
                            _(
                                '''Ошибка!<br>
                                %s<br><br>
                                <a href='/admin/'>Назад в админку</a>'''
                            ) % e,
                            content_type='text/html'
                        )

                Menu.objects.rebuild()

                return  # Ничего не возвращаем, это вернет нас на список товаров
        else:
            form = MenuParentForm()
        return render(
            request,
            'admin/set_parent.html',
            {
                'title': _('Укажите родительский пункт меню, под который нужно переместить выбранные страницы'),
                'objects': queryset, 'form': form
            }
        )
    set_parent_action.short_description = _('Переместить выбранные страницы в родительскую категорию')


admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)
