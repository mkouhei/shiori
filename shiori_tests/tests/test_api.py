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
        User.objects.create_user(v.username, v.email, v.password)
        User.objects.create_user(v.username2, v.email2, v.password2)
        self.client.login(username=v.username, password=v.password)

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
        payload = {'tag': v.tag0}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)

    def test_get_tags(self):
        payload = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload))
        response = self.client.get('/v1/tags')
        self.assertEqual(response.status_code, 200)

    def test_get_tag(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.get('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 200)

    def test_delete_tag(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_tag(self):
        payload = {'tag': v.tag0}
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

    def test_get_tags_by_anonymous(self):
        payload = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload))

        self.client.logout()
        r = self.client.get('/v1/tags')
        self.assertEqual(r.status_code, 200)

        id = json.loads(r.content).get('results')[0].get('id').encode('utf-8')
        response = self.client.get('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 200)

    def test_post_tags_by_anonymous(self):
        self.client.logout()
        payload = {'tag': v.tag0}
        response = self.client.post('/v1/tags',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_tag_by_anonymous(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_tag_by_anonymous(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        payload2 = {'id': id,
                    'tag': v.tag2}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_delete_tag_by_another_user(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.delete('/v1/tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_put_tag_by_another_user(self):
        payload = {'tag': v.tag0}
        r = self.client.post('/v1/tags',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        payload2 = {'id': id, 'tag': v.tag2}
        response = self.client.put('/v1/tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 403)

    def test_post_category(self):
        payload = {'category': v.category0}
        response = self.client.post('/v1/categories',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 201)

    def test_delete_category(self):
        payload = {'category': v.category0}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_category(self):
        payload = {'category': v.category0}
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

    def test_get_categories_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        self.client.logout()
        r = self.client.get('/v1/categories')
        self.assertEqual(r.status_code, 200)

        id = json.loads(r.content).get('results')[0].get('id').encode('utf-8')
        response = self.client.get('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 200)

    def test_post_category_by_anonymous(self):
        self.client.logout()
        payload = {'category': v.category0}
        response = self.client.post('/v1/categories',
                                    content_type='application/json',
                                    data=json.dumps(payload))
        self.assertEqual(response.status_code, 403)

    def test_delete_category_by_anonymous(self):
        payload = {'category': v.category0}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_category_by_anonymous(self):
        payload = {'category': v.category0}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        payload2 = {'id': id,
                    'category': v.category2}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_delete_category_by_another_user(self):
        payload = {'category': v.category0}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.delete('/v1/categories/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_put_category_by_another_user(self):
        payload = {'category': v.category0}
        r = self.client.post('/v1/categories',
                             content_type='application/json',
                             data=json.dumps(payload))
        id = json.loads(r.content).get('id').decode('utf-8')

        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        payload2 = {'id': id, 'category': v.category2}
        response = self.client.put('/v1/categories/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload2))
        self.assertEqual(response.status_code, 403)

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
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload2))
        self.assertEqual(response.status_code, 201)

    def test_delete_bookmark(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        r = self.client.post('/v1/bookmarks',
                             content_type='application/json',
                             data=json.dumps(payload2))
        id = json.loads(r.content).get('id').decode('utf-8')
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload2 = {'category': v.category2}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
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
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        response = self.client.post('/v1/bookmark_tags',
                                    content_type='application/json',
                                    data=json.dumps(payload4))
        self.assertEqual(response.status_code, 201)

    def test_delete_bookmark_tags(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 204)

    def test_put_bookmark_tags(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'tag': v.tag2}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload4))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

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

    def test_post_bookmark_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        self.client.logout()
        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        response = self.client.post('/v1/bookmarks',
                                    content_type='application/json',
                                    data=json.dumps(payload2))
        self.assertEqual(response.status_code, 403)

    def test_delete_bookmark_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        r = self.client.post('/v1/bookmarks',
                             content_type='application/json',
                             data=json.dumps(payload2))
        id = json.loads(r.content).get('id').decode('utf-8')
        self.client.logout()
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_bookmark_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload2 = {'category': v.category2}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
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
        self.client.logout()
        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload4))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_delete_bookmark_by_another_user(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        r = self.client.post('/v1/bookmarks',
                             content_type='application/json',
                             data=json.dumps(payload2))
        id = json.loads(r.content).get('id').decode('utf-8')
        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.delete('/v1/bookmarks/%s' % id)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete('/v1/bookmarks/%s?is_all=true' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    # Url of bookmark is not unique in all users,
    # but url by users should be unique.
    @unittest.skip("ToDo skipping")
    def test_put_bookmark_by_another_user(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))
        payload2 = {'category': v.category2}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
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
        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.put('/v1/bookmarks/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload4))
        print(response.content)
        self.assertEqual(response.status_code, 403)

    def test_post_bookmark_tags_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        self.client.logout()
        response = self.client.post('/v1/bookmark_tags',
                                    content_type='application/json',
                                    data=json.dumps(payload4))
        self.assertEqual(response.status_code, 403)

    def test_delete_bookmark_tags_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        self.client.logout()
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    def test_put_bookmark_tags_by_anonymous(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'tag': v.tag2}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload4))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        payload5 = {'id': id,
                    'bookmark': v.url,
                    'tag': v.tag2}

        self.client.logout()
        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload5))
        self.assertEqual(response.status_code, 403)

    # ToDo: delete is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_delete_bookmark_tags_by_another_user(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.delete('/v1/bookmark_tags/%s' % id)
        self.assertEqual(response.status_code, 403)

    # ToDo: put is allowed by owner user only.
    @unittest.skip("ToDo skipping")
    def test_put_bookmark_tags_by_another_user(self):
        payload = {'category': v.category0}
        self.client.post('/v1/categories',
                         content_type='application/json',
                         data=json.dumps(payload))

        payload2 = {'url': v.url,
                    'title': v.title,
                    'category': v.category0,
                    'description': '',
                    'is_hide': False}
        self.client.post('/v1/bookmarks',
                         content_type='application/json',
                         data=json.dumps(payload2))

        payload3 = {'tag': v.tag0}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload3))

        payload4 = {'tag': v.tag2}
        self.client.post('/v1/tags',
                         content_type='application/json',
                         data=json.dumps(payload4))

        payload4 = {'bookmark': v.url,
                    'tag': v.tag0}

        r = self.client.post('/v1/bookmark_tags',
                             content_type='application/json',
                             data=json.dumps(payload4))

        id = json.loads(r.content).get('id')
        payload5 = {'id': id,
                    'bookmark': v.url,
                    'tag': v.tag2}

        self.client.logout()
        self.client.login(username=v.username2, password=v.password2)
        response = self.client.put('/v1/bookmark_tags/%s' % id,
                                   content_type='application/json',
                                   data=json.dumps(payload5))
        self.assertEqual(response.status_code, 403)
