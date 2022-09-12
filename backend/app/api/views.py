from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

from api.serializers import (
    UsersSerializer,
    GroupsSerializer,
    UsersProfileSerializer,
    UsersProfileFilesSerializer,
)
from django.contrib.auth.models import (
    User,
    Group,
)
from api.models import (
    app_settings,
    UserProfile,
    UserProfileFiles,
)



# Create your views here.

def index(request, *args, **kwargs):
    if not app_settings.objects.first():
        record = app_settings.objects.create()
        record.save()

    if request.user.is_authenticated:
        user_settings = app_settings.objects.filter(user=request.user).first()
        if not user_settings:
            record = app_settings.objects.create()
            record.user = request.user
            record.save()
            user_settings = record
    else:
        user_settings = app_settings.objects.filter(user__isnull=True).first()

    context = {
        'app_settings': user_settings.json_data,
    }
    template = 'spa/index.html'

    return render(request, template, context)



class UsersViewSet(viewsets.ModelViewSet):
    """
    User's data
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UsersSerializer



class UsersProfileViewSet(viewsets.ModelViewSet):
    """
    User's profile data
    """
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all().order_by('-created_at_datetime')
    serializer_class = UsersProfileSerializer



class UsersProfileFilesViewSet(viewsets.ModelViewSet):
    """
    User's profile files data
    """
    permission_classes = [IsAdminUser]
    queryset = UserProfileFiles.objects.all().order_by('-created_at_datetime')
    serializer_class = UsersProfileFilesSerializer



class GroupsViewSet(viewsets.ModelViewSet):
    """
    Group's data
    """
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupsSerializer
