# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        IsAdminUser)
from rest_framework.exceptions import NotAuthenticated
from shiori.bookmark.models import (Category,
                                    Tag,
                                    Bookmark,
                                    BookmarkTag,
                                    FeedSubscription)
from shiori.api.permissions import (IsOwnerOrReadOnly,
                                    IsAuthenticatedAndCreateReadOnly)
from shiori.api.serializers import (CategorySerializer,
                                    TagSerializer,
                                    BookmarkSerializer,
                                    BookmarkTagSerializer,
                                    FeedSubscriptionSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedAndCreateReadOnly,)

    def pre_save(self, obj):
        obj.category = escape(self.request.DATA.get('category'))


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedAndCreateReadOnly,)
    paginate_by = 50

    def pre_save(self, obj):
        obj.tag = escape(self.request.DATA.get('tag'))


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        if isinstance(self.request.user, AnonymousUser):
            raise NotAuthenticated
        else:
            obj.owner = self.request.user
        obj.title = escape(self.request.DATA.get('title'))
        obj.description = escape(self.request.DATA.get('description'))

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


class FeedSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = FeedSubscription.objects.all()
    serializer_class = FeedSubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        if isinstance(self.request.user, AnonymousUser):
            raise NotAuthenticated
        else:
            obj.owner = self.request.user

    def get_queryset(self):
        return FeedSubscription.objects.filter(owner=self.request.user)
