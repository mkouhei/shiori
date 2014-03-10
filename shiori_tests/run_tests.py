# -*- coding: utf-8 -*-
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'shiori_tests.settings'
test_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings as s


def run_tests():
    TestRunner = get_runner(s)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failuers = test_runner.run_tests(['shiori_tests.tests'])
    sys.exit(bool(failuers))

if __name__ == '__main__':
    run_tests()
