# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.views.generic import RedirectView
import django_openid_auth
import django.contrib.auth.views


class CoreTest(TestCase):

    def test_root_url_resolve(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/shiori/',
                             status_code=301, target_status_code=200)

    def test_login_url_resolv(self):
        found = resolve('/login/')
        self.assertEqual(found.func, django_openid_auth.views.login_begin)

    def test_logout_url_resolv(self):
        found = resolve('/logout/')
        self.assertEqual(found.func, django.contrib.auth.views.logout)
