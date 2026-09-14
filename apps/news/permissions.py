from rest_framework import permissions
from apps.users.models import UserRole


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access (GET) for anyone (including anonymous users),
    and full CRUD access (POST, PUT, PATCH, DELETE) strictly for users with Admin role.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            (getattr(request.user, 'role', None) == UserRole.ADMIN or request.user.is_staff or request.user.is_superuser)
        )
