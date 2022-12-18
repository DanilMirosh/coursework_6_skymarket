from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    message = "Delete or edit ads can owners or admins only."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.is_admin:
            return True
        return False
