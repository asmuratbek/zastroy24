from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', news_list, name='list'),
    url(r'^(?P<slug>[\w\-]+)/$', news_single, name='single'),

]