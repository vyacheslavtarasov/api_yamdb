from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.author)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.role == 'moderator':
                return True
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )