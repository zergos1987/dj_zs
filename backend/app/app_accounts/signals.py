from django.dispatch import receiver
from djoser.signals import user_registered
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from .models import (
        User,
        UserProfile,
        UserProfileFiles,
        SessionExtraData,
	)



# Signals



@receiver(user_registered, dispatch_uid="user_registered_userprofile_create")
def create_profile(sender, user, request, **kwargs):
    """
        Add user profile on register
    """
    data = request.data

    UserProfile.objects.create(
        user=user,
        first_name=data.get("first_name", ""),
        middle_name=data.get("middle_name", ""),
        last_name=data.get("last_name", "")
    )


@receiver(post_save, sender=User, dispatch_uid='post_save_UserProfile_create')
def post_save_UserProfile_create(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User, dispatch_uid='post_save_UserProfile_save')
def post_save_UserProfile_save(sender, instance, **kwargs):
    instance.UserProfile.save()


@receiver(post_save, sender=Session, dispatch_uid='session_post_save')
def post_save_Session(sender, instance, created, **kwargs):
    """
        Remove all old sessions from current user session
    """
    if created:
        obj, obj_created = SessionExtraData.objects.get_or_create(
            session=instance,
        )

    user_id = instance.get_decoded().get('_auth_user_id')
    # Get all sessions excluding current session
    sessions = Session.objects.exclude(session_key=instance.session_key)
    # Iterate over all sessions and decode them
    for session in sessions:
        session_user_id = session.get_decoded().get('_auth_user_id')
        # If the session belongs to user, delete it
        if session_user_id == user_id:
            session.delete()


# @receiver(user_logged_in, dispatch_uid='user_logged_in_create_user_connection_stats')
# def on_login(sender, user, request, **kwargs):
#     for i in request.META:
#         print(user, i)
#     print(request.META.get('HTTP_USER_AGENT'))
#     print('User just logged in....')
