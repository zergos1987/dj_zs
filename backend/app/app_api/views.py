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
        if request.META.get('HTTP_REFERER', None) is not None:
            if '/admin/' in request.META.get('HTTP_REFERER'):
                return redirect('/admin/login/')
        if request.user.is_authenticated:
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return Response(data={
                "Login Api": "Already authorized",
                "username": request.user.username, 
                "email": request.user.email, 
                "phone": request.user.phone
            })
        else:
            return Response(data={
                "Login Api": "Example below",
                "username": "username/email/phone", 
                "password": "*****"
            })
    
    def post(self, request):
        if request.user.is_authenticated:
            return Response(data={
                "Login Api": "Already authorized",
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "phone": request.user.phone
            })
        
        if not request.data:
            return Response(data={
                "Login Api": "Miss/invalid credentials",
                "Login": "Username/password doesn't exists",
            })
        
        if not request.user.is_authenticated and request.data:
            data = request.data
            username = data.get('username', None)
            password = data.get('password', None)
            user = None
            if username and password:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    return Response(data={
                        "Login Api": "User blocked",
                        "id": request.user.id,
                        "username": request.user.username,
                        "email": request.user.email,
                        "phone": request.user.phone
                    })
            else:
                return Response(data={
                    "Login Api": "Login failed",
                    "Login": "Username/password incorrect"
                })
            
        if request.GET.get('next'):
            if '/swagger/' in request.GET.get('next'):
                return redirect(request.GET.get('next')+'?format=openapi'
            else:
                return redirect(request.GET.get('next'))
        else:
            return Response(data={
                "Login Api": "Login success.",
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "phone": request.user.phone
            })
        
        return Response(status=HTTP_404_NOT_FOUND)
    
    
    
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
