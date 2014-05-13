# -*- coding: utf-8 -*-
""" feed parser module """
from defusedxml import lxml
from lxml.etree import XMLSyntaxError
import requests
import sys


def get_updated(etree, nsmap):
    """
    Arguments:
        etree: xml element tree
        nsmap: name space map
    Return:
        string of updated date
    """
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


def get_title(etree, namespace):
    """
    Arguments:
        etree: xml element tree
        ns: name space
    Return:
        string of title
    """
    if etree.find('.//%stitle' % namespace) is not None:
        return etree.find('.//%stitle' % namespace).text


def get_link(etree, namespace):
    """
    Arguments:
        etree: xml element tree
        ns: name space
    Return:
        string of url
    """
    if etree.find('.//%slink' % namespace) is not None:
        if etree.find('.//%slink' % namespace).get('href'):
            return etree.find('.//%slink' % namespace).get('href')
        elif etree.find('.//%slink' % namespace).text is not None:
            return etree.find('.//%slink' % namespace).text


def get_items(etree, namespace):
    """
    Arguments:
        etree: XML element tree
        ns: name space
    Return:
        object of items
    """
    if etree.find('.//%schannel/%sitem' % (namespace,
                                           namespace)) is not None:
        return etree.findall('.//%schannel/%sitem' % (namespace,
                                                      namespace))
    elif etree.find('.//%sentry' % namespace) is not None:
        return etree.findall('.//%sentry' % namespace)
    elif etree.find('.//%sitem' % namespace) is not None:
        return etree.findall('.//%sitem' % namespace)


def get_ns(nsmap, key=None):
    """
    Arguments:
        nsmap: name space map
        key: name space key
    Return:
        name space
    """
    if nsmap.get(key) is None:
        namespace = ''
    else:
        namespace = '{%s}' % nsmap.get(key)
    return namespace


class FeedParser(object):
    """ FeedParser class """

    def __init__(self, url):
        try:
            response = requests.get(url, stream=True)
        except requests.ConnectionError as error:
            print(error)
            sys.exit(1)
        try:
            etree = lxml.fromstring(response.content)
        except XMLSyntaxError as error:
            print(error)
            sys.exit(1)
        self.nsmap = etree.nsmap
        self.namespace = get_ns(etree.nsmap, None)

        self.updated = get_updated(etree, self.nsmap)
        self.title = get_title(etree, self.namespace)
        self.items = get_items(etree, self.namespace)
        self.etree = etree

    def retrieve_items(self):
        """ retrieve feed items """
        return [dict(title=get_title(item, self.namespace),
                     link=get_link(item, self.namespace),
                     updated=get_updated(item, self.nsmap))
                for item in self.items]
