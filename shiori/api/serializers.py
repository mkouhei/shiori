# -*- coding: utf-8 -*-
""" serializer of shiori.api """
from rest_framework import serializers
from shiori.bookmark.models import (Category,
                                    Tag,
                                    Bookmark,
                                    BookmarkTag,
                                    FeedSubscription)


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for shiori.bookmark.models.Category """

    class Meta(object):
        """ Meta class of CategorySerializer """
        model = Category
        fields = ('id', 'category')


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for shiori.bookmark.models.Tag """

    class Meta(object):
        """ Meta class of TagSerializer """
        model = Tag
        fields = ('id', 'tag')


class BookmarkSerializer(serializers.ModelSerializer):
    """ Serializer for shiori.bookmark.models.Bookmark """

    category = serializers.SlugRelatedField(many=False, slug_field='category')
    category_id = serializers.Field(source='category.id')
    tags = serializers.SlugRelatedField(many=True, slug_field='tag',
                                        read_only=True)
    owner = serializers.Field(source='owner.username')

    class Meta(object):
        """ Meta class of BookmarkSerializer """
        model = Bookmark
        fields = ('id', 'url', 'title', 'category', 'category_id',
                  'tags', 'registered_datetime', 'description',
                  'owner', 'is_hide')


class BookmarkTagSerializer(serializers.ModelSerializer):
    """ Serializer for shiori.bookmark.models.BookmarkTag """

    bookmark = serializers.SlugRelatedField(many=False, slug_field='url')
    tag = serializers.SlugRelatedField(many=False, slug_field='tag')

    class Meta(object):
        """ Meta class of BookmarkTagSerializer """
        model = BookmarkTag
        fields = ('id', 'bookmark', 'tag')


class FeedSubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer for shiori.bookmark.models.FeedSubscription """

    owner = serializers.Field(source='owner.username')
    default_category = serializers.SlugRelatedField(many=False,
                                                    slug_field='category')
    category_id = serializers.Field(source='category.id')

    class Meta(object):
        """ Meta class of FeedSubscriptionSerializer """
        model = FeedSubscription
        fields = ('id', 'url', 'name', 'owner', 'default_category')
