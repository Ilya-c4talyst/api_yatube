from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Проверка на автора для управления даннымиа."""

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
