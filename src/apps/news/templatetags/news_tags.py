from django import template
from apps.news.models import News


register = template.Library()


def pagination(context, page_obj, begin_pages=1, end_pages=1, before_current_pages=1, after_current_pages=1):
    # Digg-like pages
    before = max(page_obj.number - before_current_pages - 1, 0)
    after = page_obj.number + after_current_pages

    begin = page_obj.paginator.page_range[:begin_pages]
    middle = page_obj.paginator.page_range[before:after]
    end = page_obj.paginator.page_range[-end_pages:]
    last_page_number = end[-1]

    def collides(firstlist, secondlist):
        """ Returns true if lists collides (have same entries)

        >>> collides([1,2,3,4],[3,4,5,6,7])
        True
        >>> collides([1,2,3,4],[5,6,7])
        False
        """
        return any(item in secondlist for item in firstlist)

    # If middle and end has same entries, then end is what we want
    if collides(middle, end):
        end = range(max(page_obj.number-before_current_pages, 1), last_page_number+1)

        middle = []

    # If begin and middle ranges has same entries, then begin is what we want
    if collides(begin, middle):
        begin = range(1, min(page_obj.number + after_current_pages, last_page_number)+1)

        middle = []

    # If begin and end has same entries then begin is what we want
    if collides(begin, end):
        begin = range(1, last_page_number+1)
        end = []

    context.update({
        'page_obj': page_obj, 'begin': begin, 'middle': middle, 'end': end
    })

    return context


def news_sidebar():
    return {'news_list': News.objects.filter(is_public=True)[:5]}


register.inclusion_tag('news_sidebar.html')(news_sidebar)
register.inclusion_tag('paginator.html', takes_context=True)(pagination)
