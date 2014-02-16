============================================================
Shiori is bookmarking tool based on Web UI and JSON REST API
============================================================

What's "Shiori"?
----------------

This tool provides web UI and JSON REST API for bookmarking.
The API depends on django REST framework,
Web UI depends on it's API and Backbone.js.
The user registeration and login of this tool uses OpenID.

"Shiori" is means a bookmark in Japanese.
It is written "栞" in Kanji, this caracter is 0x681E in Unicode.



Requirements
------------

* Python 2.7
* Django (>= 1.6)
* Django REST framework (>= 2.3.12)
* django-shortuuidfield (>= 0.1.2)
* python-openid (>= 2.2.5)
* django_openid_auth (>= 0.5)
* django-notification (>= 1.1.1)
* jQuery (>= 1.7.2)
* underscore.js (>= 1.5.2)
* backbone.js (>= 1.1.0)
* JSON in JavaScript
* Twitter bootstrap (>= 2.0.2)

Recommends
----------

* MySQL
* python-mysqldb

Setup
-----

Install Debian packages that Shiori depends on
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shiori depends on as following.::

  $ sudo apt-get install python-django python-djangorestframework \
  python-django-shortuuidfield python-django-auth-openid \
  python-django-notification \
  libjs-jquery libjs-underscore libjs-json libjs-twitter-bootstrap


Update and rebuild libjs-backbone
"""""""""""""""""""""""""""""""""

The version of libjs-backbone in Sid is 0.9.2-4 at 2014-02-08. (1)
So you must rebuild from source package currently.::

  $ sudo apt-get build-dep libjs-backbone
  $ apt-get source libjs-backbone
  $ cd backbone-0.9.2
  $ uscan
  $ uupdate ../1.x.x.tar.gz 1.x.x
  $ cd ../backbone-1.x.x
  $ debuild -us -uc
  $ sudo dpkg -i ../libjs-backbone_1.x.x-1_all.deb

(1) http://packages.qa.debian.org/b/backbone.html


Install Shiori
^^^^^^^^^^^^^^

from source
"""""""""""
::

   $ git clone https://github.com/mkouhei/shiori.git
   $ cd shiori
   $ sudo python setup.py install


from PyPI
"""""""""
::

   $ pip install shiori

Workaround django-auth-openid someproblems
""""""""""""""""""""""""""""""""""""""""""

django-auth-openid is not support django 1.5 over now,
then you should use source debian package, and must apply some patches.::

  $ apt-get source python-django-auth-openid
  $ cd django-openid-auth-0.5
  $ patch -p1 < /path/to/shiori/misc/django-openid-auth/django1.5compat.patch
  $ patch -p1 < /path/to/shiori/misc/django-openid-auth/Change-manage-py-for-django1.6.patch
  $ patch -p1 < /path/to/shiori/misc/django-openid-auth/Change-import-modules-in-urls-for-django1.6.patch
  $ patch -p1 < /path/to/shiori/misc/django-openid-auth/Change-default-SESSSION_SERIALIZER.patch
  $ python setup.py install


Make symlinks of JavaScript Libraries
"""""""""""""""""""""""""""""""""""""

Shiori has no depended on JavaScript libraries, so make symlinks.
Executute miscs/setup.sh script.::

  $ cd /path/to/lib/python2.7/site-packages/shiori-0.x.x-py2.7.egg/shiori/static
  $ sh ../miscs/setup.sh
  $ ls -n
  total 8
  lrwxrwxrwx 1 1000 1000   30 Feb  9 09:26 backbone -> /usr/share/javascript/backbone
  drwxr-xr-x 2 1000 1000 4096 Feb  9 06:49 css
  lrwxrwxrwx 1 1000 1000   34 Feb  9 09:26 twbs -> /usr/share/twitter-bootstrap/files
  lrwxrwxrwx 1 1000 1000   28 Feb  9 09:26 jquery -> /usr/share/javascript/jquery
  drwxr-xr-x 2 1000 1000 4096 Feb  9 06:49 js
  lrwxrwxrwx 1 1000 1000   26 Feb  9 09:26 json -> /usr/share/javascript/json
  lrwxrwxrwx 1 1000 1000   32 Feb  9 09:26 underscore -> /usr/share/javascript/underscore

Configuration
-------------

You must change some values in shiori/core/settings.py.

* SECRET_KEY
* DEBUG
* ALLOWED_HOSTS
* DATABASES

Execute syncdb.::

  $ python /path/to/shiori/manage.py syncdb

Run server.::

  $ python /path/to/shiori/manage.py runserver


Development
-----------

You copy pre-commit hook scripts after git clone.::

  $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python 2.7 later and setuptools, pytest, pep8.
Below way is for Debian GNU/Linux Sid system.::

  $ sudo apt-get install python python-setuptools python-pytest pep8

Then checkout 'devel' branch for development, commit your changes.
Before pull request, execute git rebase.

See also
--------

* `django REST framework <http://www.django-rest-framework.org/>`_
* `django-openid-auth README <http://bazaar.launchpad.net/~django-openid-auth/django-openid-auth/trunk/view/head:/README.txt>`_
* `Backbone.js <http://backbonejs.org/>`_

