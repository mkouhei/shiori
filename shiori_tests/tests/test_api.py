# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
import json

from shiori.api.views import CategoryViewSet
import shiori_tests.tests.vars as v


class APITest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(v.username,
                                             v.email,
                                             v.password)
        self.client.login(username=v.username,
                          password=v.password)

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

    def test_post_tag(self):
        payload = {'tag': v.tag}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)

    def test_delete_tag(self):
        payload = {'tag': v.tag}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_tag(self):
        payload = {'tag': v.tag}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        payload2 = {'id': id,
                    'tag': v.tag2}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 200)

    def test_post_category(self):
        payload = {'category': v.category}
        response = self.client.post('/v1/categories',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)

    def test_delete_category(self):
        payload = {'category': v.category}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_category(self):
        payload = {'category': v.category}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        payload2 = {'id': id,
                    'category': v.category2}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 200)

    def test_post_bookmark_without_category(self):
        payload = {'url': v.url,
                   'title': v.title,
                   'category': '',
                   'description': '',
                   'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_post_bookmark(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload2))
        self.assertEqual(response.status_code, 201)

    def test_delete_bookmark(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        r = self.client.post('/v1/bookmarks',
                             content_type='application/json',
                             data=json.dumps(payload2))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload2 = {'category': v.category2}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        r = self.client.post('/v1/bookmarks',
                             content_type='application/json',
                             data=json.dumps(payload3))
        id = json.loads(r.content).get('id').decode('utf-8')
        payload4 = {'url': v.url,
                    'title': v.title,
                    'category': v.category2,
                    'description': v.description,
                    'is_hide': True}
        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload4))
        self.assertEqual(response.status_code, 200)

    def test_post_bookmark_tags(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag}

        response = self.client.post('/v1/bookmark_tags',
                                    content_type='application/json',
                                    data=json.dumps(payload4))
        self.assertEqual(response.status_code, 201)

    def test_delete_bookmark_tags(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark_tags(self):
        payload = {'category': v.category}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'tag': v.tag2}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload4))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        payload5 = {'id': id,
                    'bookmark': v.url,
                    'tag': v.tag2}

        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload5))
        self.assertEqual(response.status_code, 200)
