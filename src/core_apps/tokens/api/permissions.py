from rest_framework.permissions import BasePermission
from datetime import date, timedelta

from core_apps.profiles.models import Profile
from core_apps.subscriptions.models import UserSubscription


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return True

            if hasattr(request.user, "profile"):
                return request.user.profile.user_type == Profile.ADMIN
        return False


class HasActiveSubscription(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        active_subscriptions = UserSubscription.objects.filter(
            user=user, is_approved=True
        )
        if not active_subscriptions.exists():
            return False

        return True


class RegularUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = user.profile

        if profile.user_type == Profile.REGULAR:
            token_name = request.query_params.get("token_name")
            if token_name.lower() != "btc":
                return False

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            if date.fromisoformat(end_date) - date.fromisoformat(
                start_date
            ) > timedelta(days=30):
                return False

            profile.reset_daily_usage()
            return True


class SubscribedUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.profile.user_type == Profile.SUBSCRIBED:
            active_subscription = UserSubscription.objects.filter(
                user=user, is_approved=True, plan__token_access=True
            ).exists()
            if active_subscription:
                return True
        return False
