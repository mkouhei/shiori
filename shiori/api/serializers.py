# -*- coding: utf-8 -*-
from rest_framework import serializers
from bookmark.models import Category, Tag, Bookmark, BookmarkTag


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'tag')


class BookmarkSerializer(serializers.ModelSerializer):

    catogory = serializers.SlugRelatedField(many=False, slug_field='category')
    tags = serializers.SlugRelatedField(many=True, slug_field='tag',
                                        read_only=True)

    class Meta:
        model = Bookmark
        fields = ('url', 'title', 'category',
                  'tags', 'registered_datetime',
                  'updated_datetime', 'description')


class BookmarkTagSerializer(serializers.ModelSerializer):

    bookmark = serializers.SlugRelatedField(many=False, slug_field='url')
    tag = serializers.SlugRelatedField(many=False, slug_field='tag')

    class Meta:
        model = BookmarkTag
        fields = ('id', 'bookmark', 'tag')
