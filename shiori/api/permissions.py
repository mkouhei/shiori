# -*- coding: utf-8 -*-
"""
see follow url
http://www.django-rest-framework.org/api-guide/permissions#custom-permissions
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
