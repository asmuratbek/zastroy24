from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^info/contacts/$', contacts, name='contacts'),
    url(r'^info/about/company/$', about, name='about'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^info/payments/$', payment_information, name='payments_info'),
    url(r'^info/delivery/$', delivery_information, name='delivery_info'),
    url(r'^info/price-list/$', price_list, name='price_list'),
    url(r'^info/service/$', service, name='service'),
    url(r'^info/partners/$', to_partners, name='to_partners'),
    url(r'^info/reviews/$', reviews, name='reviews'),
    url(r'^feedback/$', abstract_feedback, name='feedback'),
    url(r'^info/(?P<enum>[\w-]+)/$', simple_pages, name='simple_page'),
]