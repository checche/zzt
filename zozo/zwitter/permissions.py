from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """投稿者本人"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsUserOrReadOnly(permissions.BasePermission):
    """本人"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.pk == request.user.pk)

class IsUserOrAdmin(permissions.BasePermission):
    """本人とアドミン"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.pk == request.user.pk) or bool(request.user.is_staff)
