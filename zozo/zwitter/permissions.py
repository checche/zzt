from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """投稿者本人が編集,削除できる."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user