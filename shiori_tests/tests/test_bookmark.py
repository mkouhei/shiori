# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.db import IntegrityError
import shiori.bookmark.views
from shiori.bookmark.models import Category, Tag, Bookmark
from shiori.bookmark.feeds import LatestEntries
import shiori_tests.tests.vars as v


class BookmarkTransactionTest(TransactionTestCase):
    def setUp(self):
        self.user0 = User.objects.create_user(v.username0,
                                              v.email0,
                                              v.password0)
        self.user1 = User.objects.create_user(v.username1,
                                              v.email1,
                                              v.password1)
        self.category0 = Category.objects.create(category=v.category0)
        self.category1 = Category.objects.create(category=v.category1)
        self.tag0 = Tag.objects.create(tag=v.tag0)
        self.tag1 = Tag.objects.create(tag=v.tag1)
        self.bookmark = Bookmark.objects.create(url=v.url0,
                                                title=v.title0,
                                                category=self.category0,
                                                description=v.description0,
                                                owner=self.user0)

    def test_get_categories(self):
        query = Category.objects.get(category=v.category0)
        self.assertEqual(query.__unicode__(), v.category0)
        self.assertEqual(query.__str__(), v.category0)

    def test_get_category_as_multibyte(self):
        query = Category.objects.get(category=v.category1)
        self.assertEqual(query.__unicode__(), v.category1.decode('utf-8'))
        self.assertEqual(query.__str__(), v.category1)

    def test_save_category_confilict(self):
        with self.assertRaises(IntegrityError):
            query = Category(category=v.category0)
            query.save()

    def test_save_category(self):
        query = Category(category=v.category2)
        query.save()

        query2 = Category.objects.get(category=v.category2)
        self.assertEqual(query.__str__(), v.category2)

    def test_update_category(self):
        query = Category(id=self.category0.id, category=v.category2)
        query.save()

        query2 = Category.objects.get(category=v.category2)
        self.assertEqual(query2.id, self.category0.id)

    def test_delete_category(self):
        self.category0.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(category=v.category0)

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category0.id)

    def test_get_tag(self):
        query = Tag.objects.get(tag=v.tag0)
        self.assertEqual(query.__unicode__(), v.tag0)
        self.assertEqual(query.__str__(), v.tag0)

    def test_get_tag_as_multibyte(self):
        query = Tag.objects.get(tag=v.tag1)
        self.assertEqual(query.__unicode__(), v.tag1.decode('utf-8'))
        self.assertEqual(query.__str__(), v.tag1)

    def test_save_tag_confilict(self):
        with self.assertRaises(IntegrityError):
            query = Tag(tag=v.tag1)
            query.save()

    def test_save_tag(self):
        query = Tag(tag=v.tag2)
        query.save()

        query2 = Tag.objects.get(tag=v.tag2)
        self.assertEqual(query2.__str__(), v.tag2)

    def test_update_tag(self):
        query = Tag(id=self.tag0.id, tag=v.tag2)
        query.save()
        query2 = Tag.objects.get(tag=v.tag2)
        self.assertEqual(query2.id, self.tag0.id)

    def test_delete_tag(self):
        self.tag0.delete()
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(tag=v.tag0)

        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=self.tag0.id)

    def test_get_bookmark(self):
        query = Bookmark.objects.get(url=v.url0)
        self.assertEqual(query.__str__(), v.title0)

    def test_save_bookmark_conflict(self):
        with self.assertRaises(IntegrityError):
            query = Bookmark(url=v.url0,
                             title=v.title0,
                             category=self.category0,
                             description=v.description0,
                             owner=self.user0)
            query.save()

    def test_save_bookmark_same_url_by_another_user(self):
        query = Bookmark(url=v.url0,
                         title=v.title0,
                         category=self.category0,
                         description=v.description0,
                         owner=self.user1)
        query.save()
        query = Bookmark.objects.get(url=v.url0, owner=self.user1)
        self.assertEqual(query.__str__(), v.title0)

    def test_update_bookmark(self):
        query = Bookmark(id=self.bookmark.id,
                         url=v.url1,
                         title=v.title1,
                         category=self.category1,
                         description=v.description1,
                         owner=self.user0)
        query.save()

        query2 = Bookmark.objects.get(url=v.url1, owner=self.user0)
        self.assertEqual(query2.id, self.bookmark.id)

    def test_delete_bookmark(self):
        self.bookmark.delete()
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(url=v.url0, owner=self.user0)

        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(id=self.bookmark.id, owner=self.user0)


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
