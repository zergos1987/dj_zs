from django.urls import path, re_path, include
from api import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="DJ ZS API",
      default_version='v1',
      description="API",
      contact=openapi.Contact(email="admin@dj_zs.com"),
   ),
   # if False, includes only endpoints the current user has access to
   public=False,
   permission_classes=(permissions.AllowAny,),
)



router = routers.DefaultRouter()
router.register('v1/user_profile', views.UserProfile, basename="user_profile")
#router.register('user_profile_files', views.UserProfileFiles, basename="user_profile_files")

app_name = 'api'

urlpatterns = [
    re_path(r'test_view/', views.index, name='index'),
    re_path(r'^v1/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/token/access/', TokenRefreshView.as_view(), name='token_get_access'),
    path('v1/token/both/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^', include(router.urls))
]
