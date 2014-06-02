# -*- coding: utf-8 -*-
""" View of shiori UI """
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def index(request):
    """ index view """
    return render_to_response('bookmark/index.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def profile(request):
    """ profile view """
    return render_to_response('bookmark/profile.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def add(request):
    """ add bookmark view """
    if not request.user.is_authenticated():
        return redirect('/login/')
    return render_to_response('bookmark/edit.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def categories(request):
    """ bookmark categories view """
    return render_to_response('bookmark/categories.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def category(request, category_id):
    """ category view """
    return render_to_response('bookmark/category.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def tags(request):
    """ bookmark tags view """
    return render_to_response('bookmark/tags.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def tag(request, tag_id):
    """ tag view """
    return render_to_response('bookmark/tag.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def bookmark(request, bookmark_id):
    """ bookmark view """
    return render_to_response('bookmark/bookmark.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def feed_subscription(request):
    """ feed subscription view """
    return render_to_response('bookmark/feed_subscription.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def search(request):
    """ search view """
    return render_to_response('bookmark/index.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))
