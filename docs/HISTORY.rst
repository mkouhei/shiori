History
-------

0.3.4 (2014-06-02)
^^^^^^^^^^^^^^^^^^

* Fixed pylint violations.
* Fixed the name of the dependent Python packages.

0.3.3 (2014-05-12)
^^^^^^^^^^^^^^^^^^

* Fixed bug of validators.
* Added unit test of feed_parser.

0.3.2 (2014-04-18)
^^^^^^^^^^^^^^^^^^

* Fixed #25 can not search for multi-byte string.
* Applied closure-linter, and fixed invalid Google JavaScript Style Guide.
* Fixed exclude directory for PEP8 test.

0.3.1 (2014-04-09)
^^^^^^^^^^^^^^^^^^

* Added search API and view
* Fixed category and tag query
* Changed behavior of popover

0.3.0 (2014-04-03)
^^^^^^^^^^^^^^^^^^

* Change API path /v1 to /api
* Change behavior of Category API
* Change behavior of Tag API
* Added FeedSubscription and CralingHistory models
* Added API of FeedSubscription
* Added view of subscribed feeds list and manage view
* Added register bookmarks from subscribed feeds
* Added feed parser and register of bookmark from subscribed feed by celery
* Added list display at Django admin
* Using fake name generator for test
* Change using fixtures for User, Category, Tag

0.2.7 (2014-03-15)
^^^^^^^^^^^^^^^^^^

* Fixed Fixed forbid deleting bookmark by not owner user
* Added some unit test

0.2.6 (2014-03-08)
^^^^^^^^^^^^^^^^^^

* Added toggle switch to display all bookmarks
* Fixed #12 Tags and categories that do not have a bookmark is displayed
* Fixed #13 bookmarks does not appear in the tag view
* Fixed #10 It is impossible to view the bookmarks of other users
            in the login state in the UI
* Fixed #7 URL of bookmark should be unique by user

0.2.5 (2014-03-05)
^^^^^^^^^^^^^^^^^^

* Added test REST API for anonymous user and another user
* Fixed #6 any authenticated users can change bookmarks
* Fixed #8 invalid URL of login on logout page

0.2.4 (2014-03-01)
^^^^^^^^^^^^^^^^^^

* Redirect root to /shiori/
* Add test code of routing, bookmark view, REST API
* Use django test in setup.py test
* Use tox
* Use travis-ci
* Use coverage and coverall.io

0.2.3 (2014-02-26)
^^^^^^^^^^^^^^^^^^

* Add pagination
* Remove patches of django-openid-auth why fixed at python-django-auth-openid 0.5-2

0.2.2 (2014-02-22)
^^^^^^^^^^^^^^^^^^

* Fix importing modules

0.2.1 (2014-02-16)
^^^^^^^^^^^^^^^^^^

* Remove django-notification from dependency

0.2.0 (2014-02-16)
^^^^^^^^^^^^^^^^^^

* Added feed generator
* Fixed some bugs related views

0.1.0 (2014-02-08)
^^^^^^^^^^^^^^^^^^

* First release

