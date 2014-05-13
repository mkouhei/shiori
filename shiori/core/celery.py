# -*- coding: utf-8 -*-
""" Celery for configuration """
from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiori.core.settings')

APP = Celery('core')
APP.config_from_object('django.conf:settings')
APP.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@APP.task(bind=True)
def debug_task(self):
    """ for debug celery task """
    print('Request: {0!r}'.format(self.request))
