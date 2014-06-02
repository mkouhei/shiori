# -*- coding: utf-8 -*-
""" routing for API """
from django.conf.urls import patterns, include, url
from rest_framework import routers
from shiori.api import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'bookmark_tags', views.BookmarkTagViewSet)
router.register(r'feed_subscription', views.FeedSubscriptionViewSet)

urlpatterns = patterns('shiori.api.views',
                       url(r'^', include(router.urls)),)
