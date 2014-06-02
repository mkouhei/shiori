# -*- coding: utf-8 -*-
""" Celery task module """
from celery.task import PeriodicTask
from datetime import timedelta
from shiori.bookmark.agents import feed
from shiori.core.settings import CELERY_TIMEDELTA_MINUTES


class ProcessRunner(PeriodicTask):
    """ Process Runner class """

    run_every = timedelta(minutes=CELERY_TIMEDELTA_MINUTES)

    def run(self, **kwargs):
        feed.register_bookmarks()
