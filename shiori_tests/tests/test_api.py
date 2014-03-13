# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
import unittest
import json

from shiori.api.views import CategoryViewSet
import shiori_tests.tests.vars as v


class APITest(TestCase):

    def setUp(self):
        User.objects.create_user(v.username0, v.email0, v.password0)
        User.objects.create_user(v.username1, v.email1, v.password1)
        self.client.login(username=v.username0, password=v.password0)

        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload = {'tag': v.tag1}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload = {'url': v.url0,
                   'title': v.title0,
                   'category': v.category0,
                   'description': v.description0,
                   'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload = {'url': v.url1,
                   'title': v.title1,
                   'category': v.category0,
                   'description': v.description1,
                   'is_hide': True}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload = {'bookmark': v.url0, 'tag': v.tag0}
        self.client.post('/v1/bookmark_tags',
                         content_type='application/json',
                         data=json.dumps(payload))

    def test_api_categories_url_resolve(self):
        response = self.client.get('/v1/categories')
        self.assertContains(response,
                            'results',
                            status_code=200)

    def test_api_tags_url_resolve(self):
        response = self.client.get('/v1/tags')
        self.assertContains(response,
                            'results',
                            status_code=200)

    def test_api_bookmarks_url_resolve(self):
        response = self.client.get('/v1/bookmarks')
        self.assertContains(response,
                            'results',
                            status_code=200)

    def test_api_bookmark_tags_url_resolve(self):
        response = self.client.get('/v1/bookmark_tags')
        self.assertContains(response,
                            'results',
                            status_code=200)

    def test_post_tag(self):
        payload = {'tag': v.tag2}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)

    def test_post_tag_conflict(self):
        payload = {'tag': v.tag0}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '{"tag": ["Tag with this Tag already exists."]}',
                            status_code=400)

    def test_get_tags(self):
        response = self.client.get('/v1/tags')
        self.assertContains(response,
                            '"tag": "%s"' % v.tag0,
                            status_code=200)

    def test_get_tag(self):
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.get('/v1/tags/%s' % id)
        self.assertContains(response,
                            '"tag": "%s"' % v.tag0,
                            status_code=200)

    def test_delete_tag(self):
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_tag(self):
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'tag': v.tag2}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertContains(response,
                            '"tag": "%s"' % v.tag2,
                            status_code=200)

    def test_get_tags_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/tags')
        self.assertContains(r,
                            'results',
                            status_code=200)

        id = json.loads(r.content).get('results')[0].get('id').encode('utf-8')
        response = self.client.get('/v1/tags/%s' % id)
        self.assertContains(response,
                            '"tag": "%s"' % v.tag0,
                            status_code=200)

    def test_post_tags_by_anonymous(self):
        self.client.logout()
        payload = {'tag': v.tag1}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_tag_by_anonymous(self):
        self.client.logout()

        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_tag_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'tag': v.tag1}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by admin user only.
    @unittest.skip("ToDo skipping")
    def test_delete_tag_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by admin user or anyone does not use.
    @unittest.skip("ToDo skipping")
    def test_put_tag_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)
        r = self.client.get('/v1/tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'tag': v.tag2}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_post_category(self):
        payload = {'category': v.category1}
        response = self.client.post('/v1/categories',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '"category":',
                            status_code=201)

    def test_get_categories(self):
        response = self.client.get('/v1/categories')
        self.assertContains(response,
                            '"category": "%s"' % v.category0,
                            status_code=200)

    def test_get_category(self):
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.get('/v1/categories/%s' % id)
        self.assertContains(response,
                            '"category": "%s"' % v.category0,
                            status_code=200)

    def test_delete_category(self):
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_category(self):
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'category': v.category1}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertContains(response,
                            '"category":',
                            status_code=200)

    def test_get_categories_by_anonymous(self):
        self.client.logout()
        response = self.client.get('/v1/categories')
        self.assertContains(response,
                            'results',
                            status_code=200)

    def test_get_category_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id').encode('utf-8')
        response = self.client.get('/v1/categories/%s' % id)
        self.assertContains(response,
                            '"category": "%s"' % v.category0,
                            status_code=200)

    def test_post_category_by_anonymous(self):
        self.client.logout()
        payload = {'category': v.category1}
        response = self.client.post('/v1/categories',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_category_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_category_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'category': v.category1}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by admin user or anyone does not use.
    @unittest.skip("ToDo skipping")
    def test_delete_category_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by admin user or anyone does not use.
    @unittest.skip("ToDo skipping")
    def test_put_category_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)
        r = self.client.get('/v1/categories')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id, 'category': v.category1}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_post_bookmark_without_category(self):
        payload = {'url': v.url2,
                   'title': v.title2,
                   'category': '',
                   'description': v.description2,
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_post_bookmark_without_is_hide(self):
        payload = {'url': v.url2,
                   'title': v.title2,
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': None}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '"url": "%s"' % v.url2,
                            status_code=201)

    def test_post_bookmark_without_url(self):
        payload = {'url': '',
                   'title': v.title2,
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_post_bookmark_without_title(self):
        payload = {'url': v.url2,
                   'title': '',
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_post_bookmark_without_description(self):
        payload = {'url': v.url2,
                   'title': v.url2,
                   'category': v.category0,
                   'description': '',
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '"url": "%s"' % v.url2,
                            status_code=201)

    def test_post_bookmark(self):
        payload = {'url': v.url2,
                   'title': v.title2,
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '"url": "%s"' % v.url2,
                            status_code=201)

    def test_delete_bookmark(self):
        r = self.client.get('/v1/bookmarks')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark(self):
        r = self.client.get('/v1/bookmarks')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id,
                   'url': v.url2,
                   'title': v.title2,
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': True}
        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertContains(response,
                            '"url": "%s"' % v.url2,
                            status_code=200)

    # ToDo: bookmark_tags is required owner
    def test_post_bookmark_tags(self):
        payload = {'bookmark': v.url0,
                   'tag': v.tag1}
        response = self.client.post('/v1/bookmark_tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertContains(response,
                            '"bookmark": "%s"' % v.url0,
                            status_code=201)

    def test_delete_bookmark_tags(self):
        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark_tags(self):
        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id,
                   'bookmark': v.url0,
                   'tag': v.tag1}
        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertContains(response,
                            '"bookmark": "%s"' % v.url0,
                            status_code=200)

    def test_post_bookmark_by_anonymous(self):
        self.client.logout()
        payload = {'url': v.url2,
                   'title': v.title2,
                   'category': v.category0,
                   'description': v.description2,
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_bookmark_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/bookmarks')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_bookmark_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/bookmarks')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id,
                   'url': v.url0,
                   'title': v.title1,
                   'category': v.category0,
                   'description': v.description1,
                   'is_hide': True}

        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    # [Fixed] ToDo: delete is allowed by owner user only.
    def test_delete_bookmark_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)
        r = self.client.get('/v1/bookmarks?is_all=true')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete('/v1/bookmarks/%s?is_all=true' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    # Url of bookmark is not unique in all users,
    # but url by users should be unique.
    @unittest.skip("ToDo skipping")
    def test_put_bookmark_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)

        r = self.client.get('/v1/bookmarks')
        id = json.loads(r.content).get('results')[0].get('id')

        payload = {'id': id,
                   'url': v.url0,
                   'title': v.title1,
                   'category': v.category0,
                   'description': v.description1,
                   'is_hide': True}
        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_post_bookmark_tags_by_anonymous(self):
        self.client.logout()
        payload = {'bookmark': v.url0,
                   'tag': v.tag1}
        response = self.client.post('/v1/bookmark_tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_bookmark_tags_by_anonymous(self):
        self.client.logout()

        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')

        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_bookmark_tags_by_anonymous(self):
        self.client.logout()
        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id,
                   'bookmark': v.url0,
                   'tag': v.tag1}

        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_delete_bookmark_tags_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)

        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_put_bookmark_tags_by_another_user(self):
        self.client.logout()
        self.client.login(username=v.username1, password=v.password1)

        r = self.client.get('/v1/bookmark_tags')
        id = json.loads(r.content).get('results')[0].get('id')
        payload = {'id': id,
                   'bookmark': v.url0,
                   'tag': v.tag1}
        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)
