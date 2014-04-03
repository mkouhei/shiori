# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from shiori.bookmark.models import (Bookmark,
                                    Category,
                                    FeedSubscription,
                                    CrawlingHistory)
from shiori.bookmark.agents.feed_parser import FeedParser


def register_bookmarks():

    for feed in FeedSubscription.objects.all():
        result = fetch_feeds(url=feed.url,
                             category=feed.default_category,
                             owner=feed.owner)
        CrawlingHistory(feed=feed, result=json.dumps(result)).save()


def fetch_feeds(**kwargs):
    result = []
    for entry in FeedParser(kwargs.get('url')).retrieve_items():
        rc, msg = add_item(url=entry.get('link'),
                           title=entry.get('title'),
                           category=kwargs.get('category'),
                           owner=kwargs.get('owner'))
        if rc is False and "already registered:" in msg:
            break
        result.append(dict(link=entry.get('link'),
                           rc=rc,
                           msg=msg))
    return result


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
        return True, ''
    except IntegrityError as error:
        return False, "already registered: %s" % error
