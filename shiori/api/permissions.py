# -*- coding: utf-8 -*-
"""
see follow url
http://www.django-rest-framework.org/api-guide/permissions#custom-permissions
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Permit full access Owner or anyone to read only """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAuthenticatedAndCreateReadOnly(permissions.BasePermission):
    """ Permit Creating/Reading only for authenticated users """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            if request.user.is_authenticated():
                return True
        else:
            if request.user.is_superuser:
                return True
