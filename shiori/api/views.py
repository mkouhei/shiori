# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from bookmark.models import Category, Tag, Bookmark, BookmarkTag
from api.serializers import (CategorySerializer,
                             TagSerializer,
                             BookmarkSerializer,
                             BookmarkTagSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)


class BookmarkTagViewSet(viewsets.ModelViewSet):
    queryset = BookmarkTag.objects.all()
    serializer_class = BookmarkTagSerializer
    permission_classes = (IsAuthenticated,)
