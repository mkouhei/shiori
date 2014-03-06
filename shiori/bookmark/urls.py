# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from shiori.bookmark.views import BookmarkListRedirectView
from shiori.bookmark.feeds import LatestEntries


urlpatterns = patterns('shiori.bookmark.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^index$', BookmarkListRedirectView.as_view(),
                           name='index-toggle'),
                       url(r'^profile/$', 'profile'),
                       url(r'^add/$', 'add'),
                       url(r'^categories$', 'categories'),
                       url(r'^categories/(?P<category_id>[\w.]+)$',
                           'category'),
                       url(r'^tags$', 'tags'),
                       url(r'^tags/(?P<tag_id>[\w.]+)$', 'tag'),
                       url(r'^feeds$', LatestEntries()),
                       url(r'^b/(?P<bookmark_id>[\w.]+)$', 'bookmark'),)
