# -*- coding: utf-8 -*-
import feedparser
from bookmark.models import Bookmark


def add_item(**kwargs):
    bookmark = Bookmark(url=kwargs.get('url'),
                        title=kwargs.get('title'),
                        category=kwargs.get('category'),
                        ownew=kwargs.get('owner'))
    bookmark.save()
