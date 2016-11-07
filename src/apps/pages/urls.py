from django.conf.urls import url
from .views import show_page


urlpatterns = [
    url(r"^(?P<slug>[\w-]+)/$", show_page, name='show_page'),
]

# EOF
