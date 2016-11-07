from django.shortcuts import render, get_object_or_404
from .models import Menu, Page


def show_index_page(request):
    index = get_object_or_404(Page, is_public=True, is_index=True)
    return render(request, 'index.html', {'page': index})


def show_page(request, slug):
    m = Menu.objects.select_related().get(slug=slug)

    if m.page and m.page.is_public:
        return render(request, 'content_pages/%s' % m.page.template, {'page': m.page})
    else:
        return render(request, 'not_exist.html')
