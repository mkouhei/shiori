# -*- coding: utf-8 -*-
import unittest
from mock import patch
from django.core.exceptions import ValidationError
from shiori.bookmark import validators


class ValidatorsTests(unittest.TestCase):
    @patch('socket.gethostbyname', return_value='93.184.216.119')
    @patch('socket.getaddrinfo',
           return_value=[(10, 1, 6, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0)),
                         (10, 2, 17, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0)),
                         (10, 3, 0, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0))])
    def test_validate_url(self, _mock0, _mock1):
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

    @patch('socket.gethostbyname', return_value='93.184.216.119')
    @patch('socket.getaddrinfo',
           return_value=[(10, 1, 6, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0)),
                         (10, 2, 17, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0)),
                         (10, 3, 0, '',
                          ('2606:2800:220:6d:26bf:1447:1097:aa7', 0, 0, 0))])
    def test_get_addr(self, _mock0, _mock1):
        self.assertListEqual(['93.184.216.119',
                              '2606:2800:220:6d:26bf:1447:1097:aa7'],
                             validators.getaddr('example.org'))
