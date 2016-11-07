from .views import auth_login, auth_logout, thanks, registration, \
    reset_password, activate, set_password
from .ajax import save_profile
from django.conf.urls import url


urlpatterns = [
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),
    url(r'^thanks/$', thanks, name='thanks'),
    url(r'^profile/save/$', save_profile, name='save_profile'),
    url(r'^profile/$', save_profile, name='show_profile'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^activate/(?P<key>\w+)$', activate, name='activate'),
    url(r'^set_password/(?P<key>\w+)$', set_password, name='set_password'),
]
