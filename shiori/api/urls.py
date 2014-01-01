# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from rest_framework import routers, authtoken
from api import views

router = routers.DefaultRouter(trailing_slash=False)
urlpatterns = patterns('api.views',
                       url(r'^', include(router.urls)),
                       )
urlpatterns += patterns('',
                        url(r'auth$',
                            'rest_framework.authtoken.views.obtain_auth_token')
                        )
