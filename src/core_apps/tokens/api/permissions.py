from rest_framework.permissions import BasePermission

from core_apps.profiles.models import Profile


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return True

            if hasattr(request.user, "profile"):
                return request.user.profile.user_type == Profile.ADMIN
        return False
