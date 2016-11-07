from django.conf.urls import url
from .views import news_list, news_detail


urlpatterns = [
    url(r"^$", news_list, name="news_list"),
    url(r"^(?P<pk>\d+)/$", news_detail, name="news_detail"),
]
