# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import LoginForm, RegisterForm
from client_app.utils import generate_view_params, send_email_notification

# Create your views here.
from users.models import User


def sign_out(request):
    logout(request)
    response = redirect('/')
    return response

    return response


def sign_in(request):
    _form = LoginForm()
    messages = None
    if request.POST:
        _form = LoginForm(request.POST)
        if _form.is_valid():
            messages = list()
            email = _form.cleaned_data['email']
            password = _form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    messages.append('User is not active')
            else:
                messages.append('Login or password is incorrect')

    params = {
        'form': _form,
        'messages': messages
    }
    params.update(generate_view_params(request))
    return render(request, 'account/login.html', params)


def get_site_url(request):
    return request.get_host()


def sign_up(request):
    _form = RegisterForm()
    messages = None

    if request.POST:
        _form = RegisterForm(request.POST)
        messages = list()
        if _form.is_valid():
            print _form.cleaned_data

            try:
                user = User.objects.get(email=_form.cleaned_data['email'])
                messages.append('This email already used!')
            except ObjectDoesNotExist:
                user = User(
                    email=_form.cleaned_data['email'],
                    password=make_password(_form.cleaned_data['password2']),
                    is_active=False
                )
                user.save()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                template = loader.get_template('account/partial/confirm_email.html')
                protocol = 'https://' if request.is_secure() else 'http://'
                contexts = {
                    'link': protocol + request.get_host() + reverse('users:users_confirm',
                                                               kwargs={'uidb64': uid, 'token': token})
                }
                response = template.render(contexts, request)
                print contexts
                thread = threading.Thread(target=send_email_notification, args=(
                    'Activating profile | MyBrands.kg',
                    response,
                    [user.email],

                ))

                thread.start()
                messages.append('We sent message with activation link on your email!')

        else:
            messages.append('Somethings goes wrong... Please check the form for correctness of the filled data')
            messages.append(_form.error_messages)

    params = {
        'form': _form,
        'messages': messages
    }
    params.update(generate_view_params(request))
    return render(request, 'account/register.html', params)


def confirm_email(request, uidb64, token):
    messages = list()
    if uidb64 is not None and token is not None:
        uid = urlsafe_base64_decode(uidb64)
        try:
            user = User.objects.get(pk=uid)
            if not user.is_active:
                if default_token_generator.check_token(user, token):
                    user.is_active = True
                    login(request, user)
                    messages.append('You have successfully activated your profile!')
                else:
                    messages.append('Link is incorrect')
            else:
                messages.append('Link is deprecated')
        except ObjectDoesNotExist:
            messages.append('User not found...')
    else:
        messages.append('Data is empty!')

    params = {
        'messages': messages
    }
    params.update(generate_view_params(request))
    return render(request, 'account/activate.html', params)


@login_required
def profile(request):
    params = {
        'user': request.user
    }
    params.update(generate_view_params(request))
    return render(request, 'account/profile.html', params)


