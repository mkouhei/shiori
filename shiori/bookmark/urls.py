# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('bookmark.views',
                       url(r'^$', 'index'),
                       url(r'^profile/$', 'profile'),
                       url(r'^categories/$', 'categories'),
                       url(r'^tags/$', 'tags'),)
