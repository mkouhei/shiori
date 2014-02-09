# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       (r'', include('django_openid_auth.urls')),
                       (r'^openid/', include('django_openid_auth.urls')),
                       (r'^logout/$', 'django.contrib.auth.views.logout',
                        {'template_name': 'bookmark/logout.html'}),
                       (r'^v1/', include('api.urls')),
                       (r'^shiori/', include('bookmark.urls')),
                       url(r'^admin/', include(admin.site.urls)),)
