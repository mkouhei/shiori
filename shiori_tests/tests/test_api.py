# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from shiori.api.views import CategoryViewSet


class APITest(TestCase):

    def test_api_categories_url_resolve(self):
        response = self.client.get('/v1/categories')
        self.assertEqual(response.status_code, 200)

    def test_api_tags_url_resolve(self):
        response = self.client.get('/v1/tags')
        self.assertEqual(response.status_code, 200)

    def test_api_bookmarks_url_resolve(self):
        response = self.client.get('/v1/bookmarks')
        self.assertEqual(response.status_code, 200)

    def test_api_bookmark_tags_url_resolve(self):
        response = self.client.get('/v1/bookmark_tags')
        self.assertEqual(response.status_code, 200)
