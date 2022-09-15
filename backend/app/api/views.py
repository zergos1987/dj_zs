from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

from serializers.users import (
    UsersSerializer,
    GroupsSerializer,
    UsersProfileSerializer,
    UsersProfileFilesSerializer,
)
from django.contrib.auth.models import (
    # User,
    Group,
)
from accounts.models import (
    User,
    UserProfile,
    UserProfileFiles,
)



# Create your views here.



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
