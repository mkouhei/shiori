==========================
Shiori is bookmarking tool
==========================

What's "Shiori"?
----------------

"Shiori" is means a bookmark. It is written "栞" in Kanji, this caracter is 0x681E in Unicode.
 
Shiori is that written later. 


Requirements
------------

* Python 2.7
* Django
* Django REST framework
* django-shortuuidfield
* django_openid_auth
* South


Setup
-----

Install Debian packages that Shiori depends on
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shiori depends on as following:

  $ sudo apt-get install python-django python-djangorestframework \
  python-django-shortuuidfield python-django-south


Install Shiori
^^^^^^^^^^^^^^

Install that choosing with one of three ways.

from source
"""""""""""
::

   $ git clone https://github.com/mkouhei/shiori.git
   $ cd shiori
   $ sudo python setup.py install


PyPI
""""
::

   $ pip install shiori

Debian package 
"""""""""""""""

Not yet official package, then download python-shiori-x.x_all.deb from https://github.com/mkouhei/shiori/downloads and install with dpkg command.::

  $ wget https://github.com/mkouhei/iori/download/python-shiori_x.x-x_all.deb
  $ sudo dpkg -i python-shiori_x.x-x_all.deb


Development
-----------

You copy pre-commit hook scripts after git clone.::

  $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python 2.7 later and setuptools, pytest, pep8. Below way is for Debian GNU/Linux Sid system.::

  $ sudo apt-get install python python-setuptools python-pytest pep8

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.

See also
--------

* `Tumblr API <http://www.tumblr.com/docs/en/api/v2>`_

See also these documents.

