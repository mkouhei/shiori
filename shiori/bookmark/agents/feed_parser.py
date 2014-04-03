# -*- coding: utf-8 -*-
from defusedxml import lxml
from lxml.etree import XMLSyntaxError
import requests
import sys


def get_updated(etree, nsmap):
    if etree.find('.//%slastBuildDate' % get_ns(nsmap)) is not None:
        return etree.find('.//%slastBuildDate' % get_ns(nsmap)).text
    elif etree.find('.//%supdated' % get_ns(nsmap)) is not None:
        return etree.find('.//%supdated' % get_ns(nsmap)).text
    elif etree.find('.//%spublished' % get_ns(nsmap)) is not None:
        return etree.find('.//%spublished' % get_ns(nsmap)).text
    elif etree.find('.//%spubDate' % get_ns(nsmap)) is not None:
        return etree.find('.//%spubDate' % get_ns(nsmap)).text
    elif etree.find('.//%sdate' % get_ns(nsmap, 'dc')) is not None:
        return etree.find('.//%sdate' % get_ns(nsmap, 'dc')).text


def get_title(etree, ns):
    if etree.find('.//%stitle' % ns) is not None:
        return etree.find('.//%stitle' % ns).text


def get_link(etree, ns):
    if etree.find('.//%slink' % ns) is not None:
        if etree.find('.//%slink' % ns).get('href'):
            return etree.find('.//%slink' % ns).get('href')
        elif etree.find('.//%slink' % ns).text is not None:
            return etree.find('.//%slink' % ns).text


def get_items(etree, ns):
    if etree.find('.//%schannel/%sitem' % (ns, ns)) is not None:
        return etree.findall('.//%schannel/%sitem' % (ns, ns))
    elif etree.find('.//%sentry' % ns) is not None:
        return etree.findall('.//%sentry' % ns)
    elif etree.find('.//%sitem' % ns) is not None:
        return etree.findall('.//%sitem' % ns)


def get_ns(nsmap, key=None):
    if nsmap.get(key) is None:
        ns = ''
    else:
        ns = '{%s}' % nsmap.get(key)
    return ns


class FeedParser(object):

    def __init__(self, url):
        try:
            response = requests.get(url, stream=True)
        except requests.ConnectionError as e:
            print(e)
            sys.exit(1)
        try:
            etree = lxml.fromstring(response.content)
        except XMLSyntaxError as e:
            print(e)
            sys.exit(1)
        self.nsmap = etree.nsmap
        self.ns = get_ns(etree.nsmap, None)

        self.updated = get_updated(etree, self.nsmap)
        self.title = get_title(etree, self.ns)
        self.items = get_items(etree, self.ns)
        self.etree = etree

    def retrieve_items(self):
        return [dict(title=get_title(item, self.ns),
                     link=get_link(item, self.ns),
                     updated=get_updated(item, self.nsmap))
                for item in self.items]
