# -*- coding: utf-8 -*-
import unittest
from django.core.exceptions import ValidationError
from shiori.bookmark import validators


class ValidatorsTests(unittest.TestCase):
    def test_validate_url(self):
        self.assertTrue(validators.validate_url('http://example.org'))

    def test_validate_url_of_localhost(self):
        self.assertRaises(ValidationError,
                          validators.validate_url,
                          'http://localhost')

    def test_validate_url_of_not_found(self):
        self.assertRaises(ValidationError,
                          validators.validate_url,
                          'http://hoge.example.org')

    def test_validate_url_of_loopback_addr(self):
        self.assertRaises(ValidationError,
                          validators.validate_url,
                          'http://127.0.0.1')

    def test_get_addr(self):
        self.assertListEqual(['93.184.216.119',
                              '2606:2800:220:6d:26bf:1447:1097:aa7'],
                             validators.getaddr('example.org'))
