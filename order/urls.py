from django.conf.urls import url
from .views import *


urlpatterns = [
    url(
        r'^basket/$',
        list_basket,
        name='basket_list'
    ),
    url(
        r'^basket/add/(?P<p_slug>[\w\-]+)/$',
        add_to_basket,
        name='basket_add'
    ),
    url(
        r'^basket/remove/(?P<b_id>[0-9]+)/$',
        remove_from_basket,
        name='basket_remove'
    ),
    url(
        r'^basket/count/update/(?P<b_id>[\w\-]+)/$',
        update_quantity_of_basket_item,
        name='add_count'
    ),
    url(
        r'^basket/total-price/get/$',
        get_total_basket_price,
        name='get_total_basket_price'
    ),
    url(
        r'^basket/clear/$',
        clean_basket,
        name='clean_basket'
    ),
    url(
        r'^comparison/$',
        list_of_comparison,
        name='comparison_list'
    ),
    url(
        r'^comparison/(?P<p_slug>[\w-]+)/$',
        add_to_comparison,
        name='comparison_add_delete'
    ),
    url(
        r'^basket/checkout/$',
        checkout,
        name='checkout'
    )
]
