# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from shortuuidfield import ShortUUIDField


class BaseObject(models.Model):
    id = ShortUUIDField(primary_key=True, auto=True, verbose_name='UUID')

    class Meta:
        abstract = True


class Category(BaseObject):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'category'

    def __unicode__(self):
        return self.category


class Tag(BaseObject):
    tag = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'tag'

    def __unicode__(self):
        return self.tag


class Bookmark(BaseObject):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, through='BookmarkTag')
    registered_datetime = models.DateTimeField(auto_now=True,
                                               auto_now_add=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    is_hide = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookmark'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/shiori/b/%s" % self.id


class BookmarkTag(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.ForeignKey(Bookmark,
                                 db_column='bookmark_id',
                                 to_field='id')
    tag = models.ForeignKey(Tag,
                            db_column='tag_id',
                            to_field='id')

    class Meta:
        db_table = 'bookmark_tag'
        unique_together = ('bookmark', 'tag')
