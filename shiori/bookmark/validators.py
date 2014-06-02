# -*- coding: utf-8 -*-
""" module for validataion of agent """
from django.core.exceptions import ValidationError
import sys
if sys.version_info > (3, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
from netaddr import IPAddress, AddrFormatError
from socket import gaierror, gethostbyname, getaddrinfo, AF_INET6
from shiori.core.settings import FEED_EXCLUDE_FQDN


def validate_url(value):
    """
    Argument:
        value: url (eg. http://example.org/rss)
    Return:
        True or raise exceptions
    """
    hostname = urlparse(value).netloc
    if ':' in hostname:
        hostname = hostname.split(':')[0]
    if hostname in FEED_EXCLUDE_FQDN:
        raise ValidationError('%s is prohibited in FEED_EXCLUDE_FQDN.' % value)
    try:
        if IPAddress(hostname).is_loopback():
            raise ValidationError('loopback address is prohibited.')
    except AddrFormatError:
        if getaddr(hostname) == []:
            raise ValidationError('%s is not found.' % value)
        for ipaddr in getaddr(hostname):
            if IPAddress(ipaddr).is_loopback():
                raise ValidationError('loopback address is prohibited.')
    if getaddr(hostname) == []:
        raise ValidationError('%s is not found.' % value)
    return True


def getaddr(hostname):
    """
    Argument:
        hostname: FQDN (eg. example.org)
    Return:
        list of IPv4 or/and IPv6 addresses
    """
    addresses = []
    try:
        addresses.append(gethostbyname(hostname))
    except TypeError as error:
        print(error)
    except gaierror as error:
        print(error)
    try:
        addresses.append(getaddrinfo(hostname, None, AF_INET6)[0][4][0])
    except TypeError as error:
        print(error)
    except gaierror as error:
        print(error)
    return addresses
