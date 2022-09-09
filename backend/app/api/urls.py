from django.urls import path, re_path, include
from api import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register('user_profile', views.UserProfile, basename="user_profile")
#router.register('user_profile_files', views.UserProfileFiles, basename="user_profile_files")

app_name = 'api'

urlpatterns = [
    re_path(r'test_view/', views.index, name='index'),
    path('token/access/', TokenRefreshView.as_view(), name='token_get_access'),
    path('token/both/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^', include(router.urls))
]
