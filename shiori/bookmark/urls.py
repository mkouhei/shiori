# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('bookmark.views',
                       url(r'^$', 'index'),
                       url(r'^profile/$', 'profile'),
                       url(r'^categories/$', 'categories'),
                       url(r'^categories/(?P<category_id>[\w.]+)$',
                           'category'),
                       url(r'^tags/$', 'tags'),
                       url(r'^tags/(?P<tag_id>[\w.]+)$', 'tag'),)
