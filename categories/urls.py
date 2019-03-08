from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        r'^create/$',
        create_category,
        name='create'
    ),
    url(
        r'^(?P<category_slug>[\w-]+)/$',
        parent_category,
        name='parent_category'
    ),
    url(
        r'^(?P<category_slug>[\w-]+)/(?P<second_category_slug>[\w-]+)/$',
        second_level_category,
        name='second_level_category'
    ),
    url(
        r'^(?P<category_slug>[\w-]+)/(?P<second_category_slug>[\w-]+)/(?P<third_category_slug>[\w-]+)/$',
        third_level_category,
        name='third_level_category'
    )
]