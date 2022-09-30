from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    # for object level permissions
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user or request.user.is_staff) and request.user.is_active


class IsStaffUserOrAdmin(permissions.BasePermission):
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_active

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff and request.user.is_active


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser and request.user.is_active

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser and request.user.is_active
      

class IsTestUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        is_testuser = False
        return is_testuser and request.user.is_active

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        is_testuser = False
        return is_testuser and request.user.is_active
