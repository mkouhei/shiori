# -*- coding: utf-8 -*-
""" module of feed generator """
from django.contrib.syndication.views import Feed
from shiori.bookmark.models import Bookmark


class LatestEntries(Feed):
    """ Feed generator class """
    title = 'Shiori new bookmarks'
    link = '/shiori/'
    description = 'Updates on changes and additions to Shiori.'
    description_template = 'feeds/latest_title.html'

    def items(self):
        """ Retrieve latest 5 bookmarks """
        return Bookmark.objects.order_by('-registered_datetime')[:5]
