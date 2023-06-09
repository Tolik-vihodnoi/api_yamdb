from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для администратора или на чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAdminModeratorAuthor(permissions.BasePermission):
    """Разрешение для администратора, модератора
    или автора.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_moderator
                     or request.user.is_admin
                     or obj.author == request.user))


class IsAdminUser(permissions.BasePermission):
    """Разрешение для администратора."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)
