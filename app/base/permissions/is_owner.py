from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
