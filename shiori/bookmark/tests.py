# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
import bookmark.views


class BookmarkTest(TestCase):
    def test_shiori_url_resolve(self):
        found = resolve('/shiori/')
        self.assertEqual(found.func, bookmark.views.index)

    def test_profile_url_resolve(self):
        found = resolve('/shiori/profile/')
        self.assertEqual(found.func, bookmark.views.profile)

    def test_add_url_resolve(self):
        found = resolve('/shiori/add/')
        self.assertEqual(found.func, bookmark.views.add)

    def test_categories_url_resolve(self):
        found = resolve('/shiori/categories')
        self.assertEqual(found.func, bookmark.views.categories)

    def test_category_url_resolve(self):
        found = resolve('/shiori/categories/dummy_id')
        self.assertEqual(found.func, bookmark.views.category)

    def test_tags_url_resolve(self):
        found = resolve('/shiori/tags')
        self.assertEqual(found.func, bookmark.views.tags)

    def test_tag_url_resolve(self):
        found = resolve('/shiori/tags/dummy_id')
        self.assertEqual(found.func, bookmark.views.tag)

    def test_feeds_url_resolve(self):
        response = self.client.get('/shiori/feeds')
        self.assertEqual(response.status_code, 200)

    def test_bookmark_url_resolve(self):
        found = resolve('/shiori/b/dummy_id')
        self.assertEqual(found.func, bookmark.views.bookmark)
