# -*- coding: utf-8 -*-
""" routing of bookmark app """
from django.conf.urls import patterns, url
from shiori.bookmark.feed_generator import LatestEntries


urlpatterns = patterns('shiori.bookmark.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^profile/$', 'profile'),
                       url(r'^add/$', 'add'),
                       url(r'^categories$', 'categories'),
                       url(r'^categories/(?P<category_id>[\w.]+)$',
                           'category'),
                       url(r'^tags$', 'tags'),
                       url(r'^tags/(?P<tag_id>[\w.]+)$', 'tag'),
                       url(r'^feeds$', LatestEntries()),
                       url(r'^feed_subscription$', 'feed_subscription'),
                       url(r'^search$', 'search'),
                       url(r'^b/(?P<bookmark_id>[\w.]+)$', 'bookmark'),)
