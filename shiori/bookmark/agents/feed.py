# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import IntegrityError
from shiori.bookmark.models import Bookmark, Category, FeedSubscription
from shiori.bookmark.agents.feed_parser import FeedParser


def register_bookmarks():

    for feed in FeedSubscription.objects.all():
        fetch_feeds(url=feed.url,
                    category=feed.default_category,
                    owner=feed.owner)


def fetch_feeds(**kwargs):
    for entry in FeedParser(kwargs.get('url')).retrieve_items():
        add_item(url=entry.get('link'),
                 title=entry.get('title'),
                 category=kwargs.get('category'),
                 owner=kwargs.get('owner'))


def add_categories(url):
    [add_category(entry.get('category'))
     for entry
     in FeedParser(url).retrieve_items()
     if entry.get('category')]


def add_item(**kwargs):
    category = Category.objects.get(category=kwargs.get('category'))
    owner = User.objects.get(username=kwargs.get('owner'))

    bookmark = Bookmark(url=kwargs.get('url'),
                        title=kwargs.get('title'),
                        category=category,
                        owner=kwargs.get('owner'))
    try:
        bookmark.save()
    except IntegrityError as error:
        # debug_print("already registered: %s" % error)
        pass
