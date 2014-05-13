# -*- coding: utf-8 -*-
""" Registre Bookmark for django celery task """
from django.contrib.auth.models import User
from django.db import IntegrityError
import json
from shiori.bookmark.models import (Bookmark,
                                    Category,
                                    FeedSubscription,
                                    CrawlingHistory)
from shiori.bookmark.agents.feed_parser import FeedParser


def register_bookmarks():
    """ register bookmarks """
    for feed in FeedSubscription.objects.all():
        result = fetch_feeds(url=feed.url,
                             category=feed.default_category,
                             owner=feed.owner)
        CrawlingHistory(feed=feed, result=json.dumps(result)).save()


def fetch_feeds(**kwargs):
    """ fetching feeds.
    Arguments:
        url: feed entry url
        category: feed entry category
        owner: feed subscriber user
    Return:
        List of Feeds data
    """
    result = []
    for entry in FeedParser(kwargs.get('url')).retrieve_items():
        return_code, msg = add_item(url=entry.get('link'),
                                    title=entry.get('title'),
                                    category=kwargs.get('category'),
                                    owner=kwargs.get('owner'))
        if return_code is False and "already registered:" in msg:
            break
        result.append(dict(link=entry.get('link'),
                           rc=return_code,
                           msg=msg))
    return result


def add_item(**kwargs):
    """ Adding bookmark.
    Arguments:
        url: feed entry url
        title: feed entry title
        category: feed etnry category
        owner: feed subscriber user
    Return:
        (Bool, error message)
    """
    category = Category.objects.get(category=kwargs.get('category'))
    owner = User.objects.get(username=kwargs.get('owner'))
    bookmark = Bookmark(url=kwargs.get('url'),
                        title=kwargs.get('title'),
                        category=category,
                        owner=owner)
    try:
        bookmark.save()
        return True, ''
    except IntegrityError as error:
        return False, "already registered: %s" % error
