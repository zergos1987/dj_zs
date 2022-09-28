from django.urls import path, re_path, include
from app_api import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect
from django.utils.safestring import mark_safe



app_name = 'app_api'
API_VERSION = 'v1'



schema_view = get_schema_view(
   openapi.Info(
      title="DJ ZS API",
      default_version=API_VERSION,
      description="API",
      contact=openapi.Contact(email="admin@dj_zs.com"),
   ),
   # if False, includes only endpoints the current user has access to
   public=False,
   permission_classes=(permissions.AllowAny,),
)

class DJZJ_APIRootView(routers.APIRootView):
    """
    Controls appearance of the API root view
    """

    def get_view_name(self) -> str:
        return "Api Root"

    def get_view_description(self, html=False) -> str:
        text = f'<a href="/api/{API_VERSION}/swagger/" rel="nofollow"><span style="color: #001fff; ">Swagger</span></a>'
        text = text + '</br>' + f'<a href="/api/{API_VERSION}/redoc/" rel="nofollow"><span  style="color: #001fff; ">Redoc</span></a>'
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text

class ApiRouter(routers.DefaultRouter):
    APIRootView = DJZJ_APIRootView

router = ApiRouter()
#router.get_api_root_view().cls.__doc__ = f"DJ ZS API {API_VERSION} http://localhost:8100/api/v1/swagger"
router.register('users', views.UsersViewSet, basename="users")
router.register('users_profile', views.UsersProfileViewSet, basename="users_profile")
router.register('users_profile_files', views.UsersProfileFilesViewSet, basename="users_profile_files")
router.register('users_groups', views.GroupsViewSet, basename="users_groups")

urlpatterns = [
    path('', lambda request: redirect(f'{API_VERSION}/', permanent=True)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    re_path(fr'^{API_VERSION}/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{API_VERSION}/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{API_VERSION}/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path(f'{API_VERSION}/token/refresh/', TokenRefreshView.as_view(), name='token_get_access'),
    # path(f'{API_VERSION}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(fr'^{API_VERSION}/', include(router.urls))
]
