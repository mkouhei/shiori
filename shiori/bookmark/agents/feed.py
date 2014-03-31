# -*- coding: utf-8 -*-
import feedparser
from django.contrib.auth.models import User
from django.db import IntegrityError
from shiori.bookmark.models import Bookmark, Category, FeedSubscription


def register_bookmarks():
    for feed in FeedSubscription.objects.all():
        fetch_feeds(url=feed.url,
                    category=feed.default_category,
                    owner=feed.owner)


def fetch_feeds(**kwargs):
    d = feedparser.parse(kwargs.get('url'))
    for entry in d.entries:
        add_item(url=entry.link,
                 title=entry.title,
                 category=kwargs.get('category'),
                 owner=kwargs.get('owner'))


def add_item(**kwargs):
    bookmark = Bookmark(url=kwargs.get('url'),
                        title=kwargs.get('title'),
                        category=kwargs.get('category'),
                        owner=kwargs.get('owner'))
    try:
        bookmark.save()
    except IntegrityError as error:
        # debug_print("already registered: %s" % error)
        pass
