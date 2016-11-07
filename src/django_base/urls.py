from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^pages/', include('apps.pages.urls', namespace='pages')),
    url(r'^news/', include('apps.news.urls', namespace='news')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.index_title = _('Панель администратора')
admin.site.site_header = admin.site.site_title = 'DjangoBase'
