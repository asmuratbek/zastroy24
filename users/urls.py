from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        r'^logout/$',
        sign_out,
        name='logout'
    ),
    url(
        r'^sign-in/$',
        sign_in,
        name='login'
    ),
    url(
        r'^sign-up/$',
        sign_up,
        name='register'
    ),
    url(
        r'^email/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        confirm_email,
        name='users_confirm'
    ),
    url(
        r'^profile/$',
        profile,
        name='profile'
    )
]