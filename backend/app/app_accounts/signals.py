from django.dispatch import receiver
from djoser.signals import user_registered
from django.db.models.signals import post_save
from django.contrib.sessions.models import Session
from .models import (
        User,
        UserProfile,
        UserProfileFiles,
	)



# Signals 



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
    
@receiver(post_save, sender=User)
def create_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_UserProfile(sender, instance, **kwargs):
    instance.UserProfile.save()

@receiver(post_save, sender=Session, dispatch_uid='session_post_save')
def post_save_Session(sender, instance, **kwargs):
    """
        Remove all old sessions from current user session
    """
    user_id = instance.get_decoded().get('_auth_user_id')
    # Get all sessions excluding current session
    sessions = Session.objects.exclude(session_key=instance.session_key)

    # Iterate over all sessions and decode them
    for session in sessions:
        session_user_id = session.get_decoded().get('_auth_user_id')
        # If the session belongs to user, delete it
        if session_user_id == user_id:
            session.delete()
