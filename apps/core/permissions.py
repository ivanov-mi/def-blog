from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins have all permissions
        if request.user.is_staff:
            return True

        # Owners have all permissions
        return obj.author == request.user


class CommentsCustomPermission(IsOwnerOrAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        # Only post creator can delete posts' comments
        if request.method == 'DELETE' and request.user == obj.post.author:
            return True

        return super().has_object_permission(request, view, obj)


class HashtagsCustomPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only admins are allowed to do DELETE/UPDATE/PATCH requests
        return request.user.is_staff


class VotesCustomPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins have all permissions
        if request.user.is_staff:
            return True

        # Author have all permissions for their own votes
        if request.user == obj.author:
            return True

        return False
