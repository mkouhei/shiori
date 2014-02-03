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

    category = serializers.SlugRelatedField(many=False, slug_field='category')
    category_id = serializers.Field(source='category.id')
    tags = serializers.SlugRelatedField(many=True, slug_field='tag',
                                        read_only=True)
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Bookmark
        fields = ('id', 'url', 'title', 'category', 'category_id',
                  'tags', 'registered_datetime', 'description',
                  'owner', 'is_hide')


class BookmarkTagSerializer(serializers.ModelSerializer):

    bookmark = serializers.SlugRelatedField(many=False, slug_field='url')
    tag = serializers.SlugRelatedField(many=False, slug_field='tag')

    class Meta:
        model = BookmarkTag
        fields = ('id', 'bookmark', 'tag')
