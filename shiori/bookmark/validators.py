# -*- coding: utf-8 -*-
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
    hostname = urlparse(value).netloc
    if ':' in hostname:
        hostname = hostname.split(':')[0]
    if hostname in FEED_EXCLUDE_FQDN:
        raise ValidationError('%s is prohibited in FEED_EXCLUDE_FQDN.' % value)
    try:
        if IPAddress(hostname).is_loopback():
            raise ValidationError('loopback address is prohibited.')
    except AddrFormatError:
        if getaddr(hostname) is None:
            raise ValidationError('%s is not found.' % value)
        for ip in getaddr(hostname):
            if IPAddress(ip).is_loopback():
                raise ValidationError('loopback address is prohibited.')
    return True


def getaddr(hostname):
    addresses = []
    try:
        addresses.append(gethostbyname(hostname))
    except TypeError as e:
        print(e)
    except gaierror as e:
        print(e)
    try:
        addresses.append(getaddrinfo(hostname, None, AF_INET6)[0][4][0])
    except gaierror as e:
        print(e)
    return addresses
