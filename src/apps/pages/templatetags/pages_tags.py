from django import template
from apps.pages.models import Menu
from apps.news.models import News
from django_base.settings import VERSION, CODENAME

register = template.Library()


def get_version():
    return VERSION


def get_codename():
    return CODENAME


def top_menu(request):
    return {
        'request': request,
        'menu_list': Menu.objects.filter(is_visible=True),
        'is_news': News.objects.filter(is_public=True).exists()
    }


register.simple_tag(get_version, name='proj_version')
register.simple_tag(get_codename, name='proj_codename')
register.inclusion_tag('units/top_menu.html')(top_menu)
