# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from django.views.generic import RedirectView
import shiori.bookmark.views
from shiori.bookmark.feeds import LatestEntries
import shiori_tests.tests.vars as v


class BookmarkTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(v.username,
                                             v.email,
                                             v.password)

    def test_shiori_url_resolve(self):
        found = resolve('/shiori/')
        self.assertEqual(found.func, shiori.bookmark.views.index)

    def test_profile_url_resolve(self):
        found = resolve('/shiori/profile/')
        self.assertEqual(found.func, shiori.bookmark.views.profile)

    def test_add_url_resolve(self):
        found = resolve('/shiori/add/')
        self.assertEqual(found.func, shiori.bookmark.views.add)

    def test_categories_url_resolve(self):
        found = resolve('/shiori/categories')
        self.assertEqual(found.func, shiori.bookmark.views.categories)

    def test_category_url_resolve(self):
        found = resolve('/shiori/categories/dummy_id')
        self.assertEqual(found.func, shiori.bookmark.views.category)

    def test_tags_url_resolve(self):
        found = resolve('/shiori/tags')
        self.assertEqual(found.func, shiori.bookmark.views.tags)

    def test_tag_url_resolve(self):
        found = resolve('/shiori/tags/dummy_id')
        self.assertEqual(found.func, shiori.bookmark.views.tag)

    def test_feeds_url_resolve(self):
        response = self.client.get('/shiori/feeds')
        self.assertEqual(response.status_code, 200)

    def test_bookmark_url_resolve(self):
        found = resolve('/shiori/b/dummy_id')
        self.assertEqual(found.func, shiori.bookmark.views.bookmark)

    def test_index_view(self):
        request = self.client.get('/shiori/')
        request.user = self.user
        response = shiori.bookmark.views.index(request)
        self.assertTrue('logout' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        request = self.client.get('/shiori/profile')
        request.user = self.user
        response = shiori.bookmark.views.profile(request)
        self.assertTrue('date joined' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_categories_view(self):
        request = self.client.get('/shiori/categories')
        request.user = self.user
        response = shiori.bookmark.views.categories(request)
        self.assertTrue('categories_list' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_category_view(self):
        request = self.client.get('/shiori/category/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.category(request, 'dummy_id')
        self.assertTrue('category_view' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_tags_view(self):
        request = self.client.get('/shiori/tags')
        request.user = self.user
        response = shiori.bookmark.views.tags(request)
        self.assertTrue('tags_list' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_tag_view(self):
        request = self.client.get('/shiori/tag/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.tag(request, 'dummy_id')
        self.assertTrue('tag_view' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_bookmark_view(self):
        request = self.client.get('/shiori/b/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.bookmark(request, 'dummy_id')
        self.assertTrue('bookmark_view' in response.content)
        self.assertEqual(response.status_code, 200)
