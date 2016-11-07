from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Tag, News
from datetime import date, datetime, timedelta


def news_list(request):
    '''
    Формируем список новостей согласно переданным параметрам
    '''
    tag = request.GET.get('t')
    page = request.GET.get('page')
    dt = request.GET.get('d')
    category = request.GET.get('c')

    c_obj = None
    t_obj = None
    cur_dt = None

    if category and not tag:
        c_obj = Category.objects.get(slug=category)
        news_list = News.news_objects.filter(category=c_obj)
    elif tag and not category:
        t_obj = Tag.objects.get(slug=tag)
        news_list = News.news_objects.filter(tags=t_obj)
    else:
        news_list = News.news_objects.all()

    if dt and dt in ['today', 'yesterday', 'week', 'month', 'year']:
        cur_dt = dt
        today = datetime.now()
        yesterday = today-timedelta(days=1)
        dt_filter = {
            'today': {'lte': today, 'gte': datetime(today.year, today.month, today.day)},
            'yesterday': {'lte': today, 'gte': datetime(yesterday.year, yesterday.month, yesterday.day)},
            'week': {'lte': today, 'gte': today-timedelta(days=today.weekday())},
            'month': {'lte': today, 'gte': date(today.year, today.month, 1)},
            'year': {'lte': today, 'gte': date(today.year, 1, 1)}
        }
        news_list = news_list.filter(pub_date__lte=dt_filter[dt]['lte'], pub_date__gte=dt_filter[dt]['gte'])

    paginator = Paginator(news_list, 15)  # Показываем 15 новостей на странице

    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:  # Если page не число - возвращаем первую страницу
        news_list = paginator.page(1)
    except EmptyPage:  # Если page слишком большое число - возвращаем последнюю страницу
        news_list = paginator.page(paginator.num_pages)

    return render(
        request,
        'news_list.html',
        {
            'news_list': news_list,
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'cur_category': c_obj,
            'cur_tag': t_obj,
            'cur_dt': cur_dt
        }
    )


def news_detail(request, pk):
    '''
    Формируем отображение детальных данных конкретной (pk) новости
    Возвращаем ошибку 404 в случае отсутсвия переданного pk в таблице новостей
    '''
    try:
        news = News.news_objects.get(pk=pk)
    except News.DoesNotExist:
        raise Http404
    return render(request, 'news_detail.html', {'news': news})
