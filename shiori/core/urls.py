# -*- coding: utf-8 -*-
""" global routing """
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       (r'', include('django_openid_auth.urls')),
                       (r'^$', RedirectView.as_view(url='/shiori/')),
                       (r'^logout/$', 'django.contrib.auth.views.logout',
                        {'template_name': 'bookmark/logout.html'}),
                       (r'^api/', include('shiori.api.urls')),
                       (r'^shiori/', include('shiori.bookmark.urls')),
                       url(r'^admin/', include(admin.site.urls)),)
