# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    return render_to_response('bookmark/index.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def profile(request):
    return render_to_response('bookmark/profile.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))


def categories(request):
    return render_to_response('bookmark/categories.html',
                              {'is_authenticated':
                               request.user.is_authenticated()},
                              context_instance=RequestContext(request))
