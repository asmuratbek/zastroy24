from django.conf.urls import url

from .views import *

urlpatterns = [
    url(
        r'^create/$',
        create_product,
        name='create'
    ),
    url(
        r'^calculator/online/$',
        calculator,
        name='calculator'
    ),
    url(
        r'^calculator/online/calculation$',
        calculation,
        name='calculation'
    ),
    url(
        r'^ajax/load-products$',
        load_products,
        name='ajax_load_products'
    ),
    url(
        r'^search/$',
        search,
        name='search'
    ),
    url(
        r'^(?P<product_slug>[\w-]+)/$',
        product_single,
        name='product_single'
    ),
    url(
        r'^(?P<slug>[\w-]+)/checkout/in/one/click/$',
        buy_on_one_click,
        name='buy_on_one_click'
    )
]
