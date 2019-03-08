"""MyBrands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from MyBrands import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from client_app import urls
from client_app.views import payments

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', include('client_app.urls', 'client_app')),
    url(r'^categories/', include('categories.urls', 'categories')),
    url(r'^products/', include('product.urls', 'products')),
    url(r'^orders/', include('order.urls', 'orders')),
    url(r'^payments/$', payments, name='payments'),
    url(r'^promotions/', include('promotions.urls', 'promotions')),
    url(r'^posts/', include('news.urls', 'news'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
