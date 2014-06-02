# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013, 2014 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
import multiprocessing


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: "
    "GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
]


long_description = (
    open("README.rst").read() +
    open(os.path.join("docs", "HISTORY.rst")).read() +
    open(os.path.join("docs", "TODO.rst")).read())

requires = ['setuptools',
            'Django',
            'djangorestframework',
            'shortuuid == 0.3.2',
            'django_shortuuidfield',
            'django-jsonfield',
            'python-openid',
            'django-openid-auth',
            'lxml',
            'defusedxml',
            'requests',
            'netaddr']

setup(name='shiori',
      version='0.3.4',
      description='bookmarking tool based on Web UI and JSON REST API',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/shiori',
      license='GNU General Public License version 3',
      classifiers=classifiers,
      packages=['shiori'],
      data_files=[],
      install_requires=requires,
      include_package_data=True,
      tests_require=['tox'],
      cmdclass={'test': Tox},)
