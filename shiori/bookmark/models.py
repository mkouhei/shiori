# -*- coding: utf-8 -*-
""" Model of bookmark """
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from shortuuidfield import ShortUUIDField
import jsonfield
from shiori.bookmark.agents.feed_parser import FeedParser
from shiori.bookmark import validators


class BaseObject(models.Model):
    """ Abstract base model that has id attribute formatted as shortuuid. """
    id = ShortUUIDField(primary_key=True, auto=True, verbose_name='UUID')

    class Meta(object):
        """ meta class """
        abstract = True


class Category(BaseObject):
    """ Category model """
    category = models.CharField(max_length=255, unique=True)

    class Meta(object):
        """ meta class """
        db_table = 'category'

    def __unicode__(self):
        return self.category


class Tag(BaseObject):
    """ Tag model """
    tag = models.CharField(max_length=255, unique=True)

    class Meta(object):
        """ meta class """
        db_table = 'tag'

    def __unicode__(self):
        return self.tag


class Bookmark(BaseObject):
    """ Bookmark model """
    url = models.URLField()
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, through='BookmarkTag')
    registered_datetime = models.DateTimeField(auto_now=True,
                                               auto_now_add=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    is_hide = models.BooleanField(default=False)

    class Meta(object):
        """ meta class """
        db_table = 'bookmark'
        unique_together = ('url', 'owner')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """ bookmark permalink path """
        return "/shiori/b/%s" % self.id


class BookmarkTag(models.Model):
    """ BookmarkTag model """
    id = models.AutoField(primary_key=True)
    bookmark = models.ForeignKey(Bookmark,
                                 db_column='bookmark_id',
                                 to_field='id')
    tag = models.ForeignKey(Tag,
                            db_column='tag_id',
                            to_field='id')

    class Meta(object):
        """ meta class """
        db_table = 'bookmark_tag'
        unique_together = ('bookmark', 'tag')


class FeedSubscription(BaseObject):
    """ FeedSubsscription model """
    url = models.URLField()
    name = models.CharField(max_length=255, editable=False)
    owner = models.ForeignKey(User)
    default_category = models.ForeignKey(Category)

    class Meta(object):
        """ meta class """
        db_table = 'feed_subscription'
        unique_together = ('url', 'owner')

    def __unicode__(self):
        return self.url


def update_title(sender, instance, **kwargs):
    """ Update title of FeedSubscription for pre_save.

    Arguments:
        sender: model (FeedSubscription)
        instance: FeedSubscription instance
        **kwargs: not use
    """
    if validators.validate_url(instance.url):
        instance.name = FeedParser(instance.url).title
    else:
        raise ValueError("Cannot insert and updating in model saving.")

pre_save.connect(update_title, sender=FeedSubscription)


class CrawlingHistory(BaseObject):
    """ Crawling History model """
    feed = models.ForeignKey(FeedSubscription)
    result = jsonfield.JSONField()
    update_datetime = models.DateTimeField(auto_now=True,
                                           auto_now_add=True)

    class Meta(object):
        """ meta class """
        db_table = 'crawling_history'

    def __unicode__(self):
        return self.id
