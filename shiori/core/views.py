# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from bookmark.models import Bookmark


def shorten_url(request, short_uri):
    obj = Bookmark.objects.get(slug=short_uri)
    return redirect(obj.url)
