# coding=utf-8
import json
import random
import shutil
import string
import threading

import os

import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from django.urls import reverse

from MyBrands import settings
from categories.models import Category, Brand
from slugify import slugify

from product.models import Product, AllProductProperties, ProductProperty, ProductImage


class Command(BaseCommand):

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    def parse_categories(self, html):
        categories = list()
        soup = BeautifulSoup(html, 'html.parser')
        categories_container = soup.find('ul', id='gtm-catalog').find_all('li', class_='submenu', recursive=False)

        for p_item in categories_container:
            p_cat = p_item.find('a', recursive=False)
            try:
                _p_cat = Category.objects.get(slug=slugify(p_cat.text))
            except ObjectDoesNotExist:
                _p_cat = Category.objects.create(title=p_cat.text, slug=slugify(p_cat.text))

            for s_item in p_item.find('div', class_='navbar-1').find('ul', class_='navbar-1__nav').find_all('li',
                                                                                                            class_='submenu',
                                                                                                            recursive=False):
                s_cat = s_item.find('a', recursive=False)
                try:
                    _s_cat = Category.objects.get(slug=slugify(s_cat.text))
                except ObjectDoesNotExist:
                    _s_cat = Category.objects.create(slug=slugify(s_cat.text), title=s_cat.text, parent_category=_p_cat)

                for t_item in s_item.find('div', class_='navbar-2').find('ul', class_='navbar-2__nav').find_all('li',
                                                                                                                class_='nav-item',
                                                                                                                recursive=False):
                    t_cat = t_item.find('a', recursive=False)
                    try:
                        _t_cat = Category.objects.get(slug=slugify(t_cat.text))
                    except ObjectDoesNotExist:
                        _t_cat = Category.objects.create(slug=slugify(t_cat.text), title=t_cat.text,
                                                         parent_category=_s_cat)

                    categories.append(dict(id=_t_cat.id, url=t_cat.get('href')))

        return categories

    def parse_category_page(self, url, cat_id):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            product_container = soup.find('div', id='category-product').find('div',
                                                                             class_='result-search').find_all(
                'div',
                class_='product-card')
        except:
            product_container = []

        for p in product_container:
            link = p.find('div', class_='product-card__name').find('a').get('href')
            thread = threading.Thread(target=self.parse_single_product_page, args=(self.get_html(link), cat_id))
            thread.start()


    def parse_single_product_page(self, html, cat_id):
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except:
            return
        try:
            article = soup.find('span', class_='product-sku-num').text.strip()
        except:
            article = random.randint(1000000, 9999999)
        try:
            title = soup.find('h1', class_='product-header').text.strip()
        except:
            title = 'Unknown product title'
        try:
            price = float(soup.find('div', id='price-less-10').find('div', class_='price-cur').find('span',
                                                                                                    class_='num').text.replace(
                ',', '.').strip().replace(' ', ''))
        except:
            price = 0
        try:
            old_price_container = soup.find('div', id='price-less-10').find('div', class_='price-old')
        except:
            old_price_container = None
        discount = 0
        if old_price_container:
            old_price = float(old_price_container.text.strip().split()[0].replace(',', '.').replace(' ', ''))
            percent_value = old_price - price
            discount = float((percent_value / old_price) * 100)

        brand = None
        try:
            characteristics_container = soup.find('div', id='product-1-inner').find('div',
                                                                                    class_='collapse-list-content').find(
                'div', class_='product-spec-wrap').find_all('div', class_='product-spec__item')
        except:
            characteristics_container = []
        characteristics = list()
        for c_item in characteristics_container:
            holder = c_item.find('dl', class_='product-spec')
            key = holder.find('dt', class_='product-spec__name').text.strip()
            value = holder.find('dd', class_='product-spec__value').text.strip()
            if key.lower() != 'бренд':
                characteristics.append(dict(
                    key=key.lower(),
                    value=value
                ))
            else:
                brand = value

        try:
            description = soup.find('div', id='product-2-inner').find('div', class_='collapse-list-content').find(
                'div').find(
                'noindex').text
        except:
            description = ""

        documentation_container = soup.find('div', id='product-3')
        documentation = None
        if documentation_container:
            tab_title = documentation_container.find('a', class_='tab-link-collaps', recursive=False).text.strip()
            if tab_title == 'документация':
                documentation = documentation_container.find(
                    'div',
                    class_='collapse-list',
                    recursive=False
                ).find(
                    'div',
                    class_='collapse-list-content',
                    recursive=False
                ).find(
                    'div',
                    recursive=False
                ).text

        images = ()
        try:
            img_container = soup.find('div', class_='product-summary-slider').find_all('div', class_='slider-item')
            for s in img_container:
                img = self.download_image(s.find('img').get('src'))
                if img:
                    images += img,
        except:
            pass

        product = dict(
            article=article,
            title=title,
            price=price,
            discount=discount,
            brand=brand,
            characteristics=characteristics,
            description=description,
            documentation=documentation,
            images=images
        )

        print(product)

        files = list()
        if len(product['images']) > 0:
            for img in product['images']:
                files.append(('files', open(img, 'rb')))

        kwargs = dict(data={
            'title': product['title'],
            'price': product['price'],
            'discount': product['discount'],
            'brand': product['brand'],
            'characteristics': json.dumps(product['characteristics']),
            'description': product['description'],
            'documentation': product['documentation'],
            'category_id': cat_id,
            'article': product['article']
        })

        brand = None
        if product['brand']:
            try:
                brand = Brand.objects.get(title=product['brand'])
            except ObjectDoesNotExist:
                brand = Brand.objects.create(title=product['brand'], slug=slugify(product['brand']))

        try:
            cat = Category.objects.get(id=cat_id)
        except ObjectDoesNotExist:
            print('Category not found....')
            return

        _product = Product()
        _product.title = product['title']
        _product.price = product['price']
        _product.discount = product['discount']
        _product.brand = brand
        _product.category = cat
        _product.description = product['description']
        _product.documentation = product['documentation']
        _product.discount = product['discount']
        _product.main_image = files[0]
        _product.save()

        for c in product['characteristics']:
            if '?' in c['key']:
                _key = c['key'].split('?')[0]
            else:
                _key = c['key']
            try:
                prop_key = AllProductProperties.objects.get(title=_key.strip().lower())
            except ObjectDoesNotExist:
                prop_key = AllProductProperties.objects.create(title=_key.strip().lower())
            if slugify(_key.strip()) == slugify('вес брутто'):
                value_holder = c['value'].strip().split()
                ProductProperty.objects.create(product=product, key=prop_key,
                                               value=float(value_holder[0].replace(',', '.')),
                                               value_type=value_holder[1])
            else:
                if '?' in c['key']:
                    ProductProperty.objects.create(product=product, key=prop_key, value=c['value'],
                                                   prop_tip=c['key'].strip().split('?')[1])
                else:
                    ProductProperty.objects.create(product=product, key=prop_key, value=c['value'])

        for img in files:
            ProductImage.objects.create(product=product, image=img)

        if os.path.exists('logs/process.log'):
            open_role = 'a'
        else:
            open_role = 'w'

        # with open('logs/process.log', open_role) as f:
        #     f.write(
        #         """
        #         =================================================================================================
        #         Product uploaded, server message: %s; \n
        #         Slug: %s; \n
        #         Category_id: %s; \n
        #         images: [%s]; \n
        #         uploading date: %s;
        #         =================================================================================================
        #         """ % (
        #             ,
        #             slugify(product['title']),
        #             cat_id,
        #             ', '.join(product['images']),
        #             str(datetime.datetime.now())
        #         )
        #     )
        #     f.close()

        for f in files:
            f[1].close()

        for i in product['images']:
            os.remove(i)

    def download_image(self, url):
        img = None

        if not os.path.exists('img'):
            os.mkdir('img')

        r = requests.get(url, stream=True)
        file_name = '%s.jpg' % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                img = file_path
        return img

    def handle(self, *args, **options):
        categories = self.parse_categories(self.get_html('http://isolux.ru/'))


        for cat in categories:
            thread = threading.Thread(target=self.parse_category_page, args=(
                cat['url'],
                cat['id']
            ))
            thread.start()
