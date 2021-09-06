from rest_framework.permissions import BasePermission

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            if request.user.is_staff or request.user.is_superuser:
                return True
            else:
                pass