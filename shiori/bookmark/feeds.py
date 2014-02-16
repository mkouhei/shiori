# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from bookmark.models import Bookmark


class LatestEntries(Feed):
    title = 'Shiori new bookmarks'
    link = '/shiori/'
    description = 'Updates on changes and additions to Shiori.'
    description_template = 'feeds/latest_title.html'

    def items(self):
        return Bookmark.objects.order_by('-registered_datetime')[:5]
