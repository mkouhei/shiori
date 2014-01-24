# -*- coding: utf-8 -*-
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from bookmark.models import Category, Tag, Bookmark, BookmarkTag
from api.serializers import (CategorySerializer,
                             TagSerializer,
                             BookmarkSerializer,
                             BookmarkTagSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 50


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Bookmark.objects.filter(is_hide=False)
        else:
            if self.request.QUERY_PARAMS.get('is_all') == 'true':
                _q = Q(is_hide=False) | Q(owner=user)
                return Bookmark.objects.filter(_q)
            else:
                return Bookmark.objects.filter(owner=user)


class BookmarkTagViewSet(viewsets.ModelViewSet):
    queryset = BookmarkTag.objects.all()
    serializer_class = BookmarkTagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
