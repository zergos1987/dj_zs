from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.views import APIView

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
from app_accounts.models import (
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
    

    
class UserLoginAPIView(APIView):
    permission_classes = []
    
    def get(self, request):
        if hasattr(request.MET, 'HTTP_REFERER'):
            if '/admin/' in request.META.get('HTTP_REFERER'):
                return redirect('/admin/login/')
        return Response(status=HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
            data = request.data
            username = data.get('username', None)
            password = data.get('password', None)
            user = None
            if username and password:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response(status=HTTP_200_OK)
                else:
                    return Response(status=HTTP_404_NOT_FOUND)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return Response(status=HTTP_200_OK)
    
    
    
class UserLogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        if request.GET.get('next'):
            print(request.GET.get('next'))
            return redirect(request.GET.get('next'))
        return Response(status=HTTP_200_OK)
