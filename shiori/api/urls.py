# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'bookmark_tags', views.BookmarkTagViewSet)

urlpatterns = patterns('api.views',
                       url(r'^', include(router.urls)),
                       )
