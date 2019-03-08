# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from client_app.forms import FeedbackForm, ReviewsForm, AffiliateFeedbackForm
from client_app.models import *
from news.models import Post
from product.models import Product, PriceList
from promotions.models import Promotion
from .utils import generate_view_params, send_email_notification
from categories.models import Brand


# Create your views here.


def index(request):
    slides = Slider.objects.all().order_by('id')
    seo_text = SeoText.objects.first()

    promotions = Promotion.objects.filter(is_active=True).order_by('-id')[:2]
    posts = Post.objects.filter(is_active=True).order_by('-created_at')[:3]

    about_us = About.objects.first()

    site_settings = SiteSettings.objects.first()

    params = {
        'location': 'home',
        'slides': slides,
        'seo_text': seo_text,
        'product_count': Product.objects.count(),
        'promotions': promotions,
        'posts': posts,
        'about_text': about_us.body if about_us else "",
        'trust': site_settings.trust if site_settings else "",
        'easy_order': site_settings.order if site_settings else "",
        'delivery': site_settings.delivery if site_settings else "",
        'easy_pay': site_settings.pay if site_settings else "",
        'i_promotions': site_settings.promotions if site_settings else ""
    }
    params.update(generate_view_params(request))
    return render(request, 'app/index.html', params)


def abstract_feedback(request):
    if request.POST:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            template = loader.get_template('app/email/feedback.html')
            context = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': email,
                'phone': form.cleaned_data['phone_number'],
                'today': datetime.today()
            }
            emails = [x.email for x in AdminEmails.objects.filter(is_active=True)]
            emails.append(email)
            response = template.render(context, request)
            thread = threading.Thread(target=send_email_notification, args=(
                'Обратная связь | Vesta Stroy',
                response,
                emails
            ))
            thread.start()

            form.save(commit=True)

            return JsonResponse(dict(
                success=True,
                message='Сообщение отправлено'
            ))
        return JsonResponse(dict(
            success=False,
            message=str(form.errors)
        ))
    return JsonResponse(dict(
        success=False,
        message='Чтобы это заработало, нужно отправить форму и POST запрос'
    ))


def contacts(request):
    affiliates = Contact.objects.all()
    params = {
        'feedback_form': AffiliateFeedbackForm(),
        'affiliates': affiliates,
        'location': 'contacts'
    }

    if request.is_ajax():
        form = AffiliateFeedbackForm(request.POST)
        if form.is_valid():
            template = loader.get_template('app/email/feedback.html')
            context = {
                'name': form.cleaned_data['name'],
                'message': form.cleaned_data['message'],
                'today': datetime.today()
            }
            emails = [form.cleaned_data['affiliate'].email]
            response = template.render(context, request)
            thread = threading.Thread(target=send_email_notification, args=(
                'Обратная связь | Vesta Stroy',
                response,
                emails
            ))
            thread.start()

            form.save(commit=True)

            return JsonResponse(dict(
                success=True,
                message='Successfully sent the message'
            ))
        return JsonResponse(dict(
            success=False,
            message=str(form.errors)
        ))

    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/contacts.html', params)


def about(request):
    about_text = About.objects.first()
    params = {
        'content': about_text,
        'location': 'about-company'
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/about-company.html', params)


import braintree
import paypalrestsdk

@csrf_exempt
def payments(request):
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "Abk1Rf3mtx3YbURcEVtzexkskze4Ggpkh2MO0PYN2oB6Bh5bWqRURBNjTFdFdkAh2VK4o_v0D6_Jwd8x",
        "client_secret": "EK_1N7EA5ui7BNDEuZuhRQ1dTcdu14GpWBQCRkyUN7on4LZmuZh1QGO8MCV9JENL0a-kpV2xmGsue92X"})
    access_token = 'access_token$sandbox$t39k5s8rk45z4rzr$6056e342d239aa6d8e53a4b2b07bf3f0'

    gateway = braintree.BraintreeGateway(access_token=access_token)
    client_token = gateway.client_token.generate()
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute",
                "cancel_url": "http://localhost:8000/"},
            "transactions": [{
                "item_list": {
                    "items": [
                        {
                            "name": "item",
                            "sku": "item",
                            "price": "5.00",
                            "currency": "USD",
                            "quantity": 1}]
                },
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")
        else:
            print(payment.error)

    context = {
        'client_token': client_token,
    }

    return render(request, 'app/paypal.html')


def subscribe(request):
    if request.is_ajax():
        email = request.POST.get('email')
        try:
            subscriber = Subscribers.objects.get(email=email)
            return JsonResponse(dict(
                success=True,
                message='Вы уже подписаны'
            ))
        except ObjectDoesNotExist:
            subscriber = Subscribers.objects.create(email=email)
            return JsonResponse(dict(
                success=True,
                message='Подписка оформлена'
            ))

    return JsonResponse(dict(
        success=False,
        message='Запрос должен быть отправлен AJAX\'ом'
    ))


def payment_information(request):
    params = {
        'location': 'payments'
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/payment-information.html', params)


def delivery_information(request):
    params = {
        'location': 'delivery',
        'info': Delivery.objects.all().order_by('id')
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/delivery-information.html', params)


def price_list(request):
    price_list = PriceList.objects.last()
    params = {
        'location': 'price-list',
        'price_list': price_list
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/price-list.html', params)


def service(request):
    params = {
        'location': 'service',
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/service-information.html', params)


def to_partners(request):
    form = FeedbackForm(request.POST)

    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            template = loader.get_template('app/email/feedback.html')
            context = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': email,
                'phone': form.cleaned_data['phone_number'],
                'today': datetime.today()
            }
            emails = [x.email for x in AdminEmails.objects.filter(is_active=True)]
            emails.append(email)
            response = template.render(context, request)
            thread = threading.Thread(target=send_email_notification, args=(
                'Обратная связь | Vesta Stroy',
                response,
                emails
            ))
            thread.start()

            form.save(commit=True)

            return JsonResponse(dict(
                success=True,
                message='Successfully sent the message'
            ))
        return JsonResponse(dict(
            success=False,
            message=str(form.errors)
        ))

    params = {
        'location': 'to-partners',
        'form': form
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/to-partners-information.html', params)


def reviews(request):
    all_visible_reviews = Reviews.objects.filter(is_active=True).order_by('id')
    form = ReviewsForm(request.POST)

    if request.POST:
        if form.is_valid():
            review = form.save(commit=True)

            template = loader.get_template('app/email/review-notification.html')
            protocol = 'https://' if request.is_secure() else 'http://'
            link = protocol + request.get_host() + reverse('admin:client_app_reviews_change', args=(review.id,))
            context = {
                'link': link
            }
            mail_body = template.render(context, request)
            thread = threading.Thread(target=send_email_notification, args=(
                'Оставили отзыв на сайте | Vesta Stroy',
                mail_body,
                [x.email for x in AdminEmails.objects.filter(is_active=True)]
            ))
            thread.start()

            return JsonResponse(dict(
                success=True,
                message='Отзыв отправлен'
            ))
        return JsonResponse(dict(
            success=False,
            message='Запрос должын быть POST!'
        ))

    params = {
        'location': 'reviews',
        'form': form,
        'reviews': all_visible_reviews
    }
    params.update(generate_view_params(request))
    return render(request, 'app/custom_pages/reviews.html', params)


def simple_pages(request, enum):
    params = {

    }

    if enum == 'manufacturers':
        params['title'] = 'Производители'
        params['content'] = Manufacturers.objects.first()
    elif enum == 'sel-terms':
        params['title'] = 'Условия продажи товаров'
        params['content'] = TermsOfSaleOfGoods.objects.first()
    elif enum == 'return-policy':
        params['title'] = 'Условия возврата товаров'
        params['content'] = ReturnPolicy.objects.first()
    elif enum == 'repair-tips':
        params['title'] = 'Советы по ремонту'
        params['content'] = RepairTips.objects.first()

    params.update(generate_view_params(request))
    return render(request, 'app/simple-page.html', params)

