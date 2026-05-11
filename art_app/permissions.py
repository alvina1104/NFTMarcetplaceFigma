from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
            getattr(request.user, 'is_seller', False))


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
            not getattr(request.user, 'is_seller', False))


class IsAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated