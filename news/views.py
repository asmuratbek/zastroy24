# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from client_app.utils import generate_view_params
from news.models import Post


# Create your views here.


def news_list(request):
    news = Post.objects.filter(is_active=True).order_by('-created_at')

    params = {
        'news': news,
    }
    params.update(generate_view_params(request))
    return render(request, 'app/news.html', params)


def news_single(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    params = {
        'post': post
    }
    params.update(generate_view_params(request))
    return render(request, 'app/news-single.html', params)
