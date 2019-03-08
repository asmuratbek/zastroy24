# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404

from client_app.utils import generate_view_params
from django.shortcuts import render
from promotions.models import Promotion

# Create your views here.


def promotions_list(request):
    params = {
        'promotions': Promotion.objects.filter(is_active=True)
    }
    params.update(generate_view_params(request))
    return render(request, 'app/promotions-list.html', params)


def promotions_single(request, slug):
    try:
        promotion = Promotion.objects.get(slug=slug)
    except:
        raise Http404

    params = {
        'promotion': promotion
    }
    params.update(generate_view_params(request))
    return render(request, 'app/promotion-single.html', params)
