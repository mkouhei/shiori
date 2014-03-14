# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.db import IntegrityError
import shiori.bookmark.views
from shiori.bookmark.models import Category, Tag
from shiori.bookmark.feeds import LatestEntries
import shiori_tests.tests.vars as v


class BookmarkTransactionTest(TransactionTestCase):
    def setUp(self):
        Category.objects.create(category=v.category0)
        Category.objects.create(category=v.category1)
        Tag.objects.create(tag=v.tag0)
        Tag.objects.create(tag=v.tag1)

    def test_categories(self):
        test0 = Category.objects.get(category=v.category0)
        self.assertEqual(test0.__unicode__(), v.category0)
        self.assertEqual(test0.__str__(), v.category0)

        test1 = Category.objects.get(category=v.category1)
        self.assertEqual(test1.__unicode__(), v.category1.decode('utf-8'))
        self.assertEqual(test1.__str__(), v.category1)

        with self.assertRaises(IntegrityError):
            t = Category(id=test0.id, category=v.category1)
            t.save()

        t = Category(id=test0.id, category=v.category2)
        t.save()

        test2 = Category.objects.get(category=v.category2)
        self.assertEqual(test2.__str__(), v.category2)
        self.assertEqual(test2.id, test0.id)

        test2.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(category=v.category2)

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=test0.id)

    def test_tags(self):
        test0 = Tag.objects.get(tag=v.tag0)
        self.assertEqual(test0.__unicode__(), v.tag0)
        self.assertEqual(test0.__str__(), v.tag0)

        test1 = Tag.objects.get(tag=v.tag1)
        self.assertEqual(test1.__unicode__(), v.tag1.decode('utf-8'))
        self.assertEqual(test1.__str__(), v.tag1)

        with self.assertRaises(IntegrityError):
            t = Tag(id=test0.id, tag=v.tag1)
            t.save()

        t = Tag(id=test0.id, tag=v.tag2)
        t.save()

        test2 = Tag.objects.get(tag=v.tag2)
        self.assertEqual(test2.__str__(), v.tag2)
        self.assertEqual(test2.id, test0.id)

        test2.delete()
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(tag=v.tag2)

        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=test0.id)


class BookmarkTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(v.username0,
                                             v.email0,
                                             v.password0)

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
        self.assertContains(response,
                            'logout',
                            status_code=200)

    def test_profile_view(self):
        request = self.client.get('/shiori/profile')
        request.user = self.user
        response = shiori.bookmark.views.profile(request)
        self.assertContains(response,
                            'date joined',
                            status_code=200)

    def test_categories_view(self):
        request = self.client.get('/shiori/categories')
        request.user = self.user
        response = shiori.bookmark.views.categories(request)
        self.assertContains(response,
                            'categories_list',
                            status_code=200)

    def test_category_view(self):
        request = self.client.get('/shiori/category/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.category(request, 'dummy_id')
        self.assertContains(response,
                            'category_view',
                            status_code=200)

    def test_tags_view(self):
        request = self.client.get('/shiori/tags')
        request.user = self.user
        response = shiori.bookmark.views.tags(request)
        self.assertContains(response,
                            'tags_list',
                            status_code=200)

    def test_tag_view(self):
        request = self.client.get('/shiori/tag/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.tag(request, 'dummy_id')
        self.assertContains(response,
                            'tag_view',
                            status_code=200)

    def test_bookmark_view(self):
        request = self.client.get('/shiori/b/dummy_id')
        request.user = self.user
        response = shiori.bookmark.views.bookmark(request, 'dummy_id')
        self.assertContains(response,
                            'bookmark_view',
                            status_code=200)
