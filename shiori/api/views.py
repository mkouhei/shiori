# -*- coding: utf-8 -*-
""" View of API """
from django.db.models import Q
from django.utils.html import escape
from django.contrib.auth.models import AnonymousUser
import sys
if sys.version_info < (3, 0):
    from urllib2 import unquote
else:
    from urllib.parse import unquote
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
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
    """ View of Category API """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedAndCreateReadOnly,)

    def pre_save(self, obj):
        obj.category = escape(self.request.DATA.get('category'))

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        elif isinstance(user, AnonymousUser):
            categories = [category.get('category')
                          for category
                          in Bookmark.objects.values('category').distinct()]
            return self.queryset.filter(id__in=categories)
        else:
            if self.request.QUERY_PARAMS.get('is_all') == 'true':

                categories = [category.get('category')
                              for category
                              in Bookmark.objects.values('category')
                              .filter(Q(owner=user) | Q(is_hide=False))
                              .distinct()]
            else:
                categories = [category.get('category')
                              for category
                              in Bookmark.objects.values('category')
                              .filter(owner=user).distinct()]
            return self.queryset.filter(id__in=categories)


class TagViewSet(viewsets.ModelViewSet):
    """ View of Tag API """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedAndCreateReadOnly,)
    paginate_by = 50

    def pre_save(self, obj):
        obj.tag = escape(self.request.DATA.get('tag'))

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        elif isinstance(user, AnonymousUser):
            bookmark = [bookmark.get('id')
                        for bookmark
                        in Bookmark.objects.values('id')
                        .filter(is_hide=False)]
            return (self.queryset.filter(bookmarktag__bookmark__in=bookmark)
                    .distinct())
        else:
            # authenticated user
            if self.request.QUERY_PARAMS.get('is_all') == 'true':
                bookmark = [bookmark.get('id')
                            for bookmark
                            in Bookmark.objects.values('id')
                            .filter(Q(owner=user) | Q(is_hide=False))]
            else:
                bookmark = [bookmark.get('id')
                            for bookmark
                            in Bookmark.objects.values('id')
                            .filter(owner=user)]
            return self.queryset\
                       .filter(bookmarktag__bookmark__in=bookmark).distinct()


class BookmarkViewSet(viewsets.ModelViewSet):
    """ View of Bookmark API """
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
            # anonymous can read all bookmarks except is_hide=True in default.
            _query = self.set_filter(Q(is_hide=False))
        elif user.is_superuser:
            # superuser can read all bookmarks in default.
            _query = self.set_filter(Q())
        else:
            # general users can read own bookmarks only in default.
            # they can read other users bookmarks when is_all=true.
            if self.request.QUERY_PARAMS.get('is_all') == 'true':
                _query = self.set_filter(Q(is_hide=False) | Q(owner=user))
            else:
                _query = self.set_filter(Q(owner=user))
        if self.request.QUERY_PARAMS.get('tag'):
            try:
                tag = Tag.objects.get(tag=self.request.QUERY_PARAMS.get('tag'))
                self.queryset = tag.bookmark_set.all()
            except Tag.DoesNotExist as exp:
                print(exp)
        return self.queryset.filter(_query)

    def set_filter(self, q_obj):
        """ filtering with query parameter """
        category = None
        if self.request.QUERY_PARAMS.get('category'):
            try:
                category = Category.objects.get(
                    category=self.request.QUERY_PARAMS.get('category'))
            except Category.DoesNotExist:
                category = None

        if category:
            q_obj = q_obj & Q(category=category)

        if self.request.QUERY_PARAMS.get('search'):
            _search = self.request.QUERY_PARAMS.get('search')
            search = unquote(_search).encode(
                'raw_unicode_escape').decode('utf-8')
            q_obj = (q_obj & Q(title__icontains=search)
                     | Q(description__icontains=search))

        return q_obj


class BookmarkTagViewSet(viewsets.ModelViewSet):
    """ View of BookmarkTag API """
    queryset = BookmarkTag.objects.all()
    serializer_class = BookmarkTagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FeedSubscriptionViewSet(viewsets.ModelViewSet):
    """ View of FeedSubscription API """
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
