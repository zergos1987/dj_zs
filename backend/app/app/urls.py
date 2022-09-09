"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib.staticfiles.views import serve



admin.site.site_header = 'DJ ZS Admin'
admin.site.index_title = 'Admin panel'
admin.site.site_title = 'DJ ZS Admin'

favicon_view = RedirectView.as_view(url='/static/assets/images/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('api/', permanent=True)),
    path('api/', include('api.urls')),
    path('spa/', include('spa.urls')),
    re_path(r'^favicon\.ico$', favicon_view),
]

if settings.DEBUG:
    import warnings

    try:
        import debug_toolbar
    except ImportError:
        warnings.warn(
            "The debug toolbar was not installed. Ignore the error. \
            settings.py should already have warned the user about it."
        )
    else:
        urlpatterns += [
            re_path(r"^__debug__/", include(debug_toolbar.urls))  # type: ignore
        ]

    urlpatterns += static("/upload/", document_root=settings.MEDIA_ROOT) + [
        re_path(r"^static/(?P<path>.*)$", serve),
    ]
