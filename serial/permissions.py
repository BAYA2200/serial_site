from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


