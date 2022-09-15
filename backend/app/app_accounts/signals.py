from django.dispatch import receiver
from djoser.signals import user_registered, user_updated

from accounts.models import UserProfile


@receiver(user_registered, dispatch_uid="create_userprofile")
def create_profile(sender, user, request, **kwargs):
    """Add user profile on register"""
    data = request.data

    UserProfile.objects.create(
        user=user,
        first_name=data.get("first_name", ""),
        middle_name=data.get("middle_name", ""),
        last_name=data.get("last_name", "")
    )