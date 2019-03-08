from django.conf.urls import url
from .views import *


urlpatterns = [
    url(
        r'^all/$',
        promotions_list,
        name='list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        promotions_single,
        name='single'
    )
]