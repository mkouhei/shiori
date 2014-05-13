# -*- coding: utf-8 -*-
import unittest
from httpretty import HTTPretty, httprettified
from defusedxml.lxml import RestrictedElement
from shiori.bookmark.agents import feed_parser


class FeedParserTests(unittest.TestCase):

    def test_retrieve_not_connect_server(self):
        with self.assertRaises(SystemExit) as e:
            parser = feed_parser.FeedParser('http://example.org/rss')
        self.assertEqual(1, e.exception.code)

    @httprettified
    def test_feedparser_not_expected_response(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               'http://example.org/rss')
        with self.assertRaises(SystemExit) as e:
            parser = feed_parser.FeedParser('http://example.org/rss')
        self.assertEqual(1, e.exception.code)

    @httprettified
    def test_feedparser_properties(self):
        with open('shiori_tests/test_data/dummy_rss.xml', 'rb') as f:
            content = f.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               'http://example.org/rss',
                               body=content)
        parser = feed_parser.FeedParser('http://example.org/rss')
        self.assertEqual({'atom': 'http://www.w3.org/2005/Atom'},
                         parser.nsmap)
        self.assertEqual('', parser.namespace)
        self.assertEqual('Sun, 11 May 2014 01:07:25 -0000',
                         parser.updated)
        self.assertEqual('Shiori new bookmarks', parser.title)
        self.assertEqual(5, len(parser.items))
        self.assertTrue(isinstance(parser.etree, RestrictedElement))

    @httprettified
    def test_retrieve_items(self):
        with open('shiori_tests/test_data/dummy_rss.xml', 'rb') as f:
            content = f.read()
        HTTPretty.register_uri(HTTPretty.GET,
                               'http://example.org/rss',
                               body=content)
        parser = feed_parser.FeedParser('http://example.org/rss')
        items = parser.retrieve_items()
        self.assertEqual(5, len(items))
