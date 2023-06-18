from rest_framework import permissions
from user.models import User


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (
                request.user.role == User.RoleChoises.ADMIN
                or request.user.role == User.RoleChoises.MODERATOR
            ):
                return True
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для работы с категориями и жанрами.
    User"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdmitOrGetOut(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
