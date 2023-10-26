"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from core import settings
from utils.modules import add_module_urls
from django.contrib import admin
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Festival Mira API",
        default_version="v1",
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=False,
)
admin.site.site_header = 'MiraMessTeam'
admin.site.index_title = "Панель администратора"
urlpatterns = [
                  url(
                      r"^apidocs(?P<format>\.json|\.yaml)$",
                      schema_view.without_ui(cache_timeout=0),
                      name="schema-json",
                  ),
                  url(
                      r"^apidocs/$",
                      login_required(schema_view.with_ui("swagger", cache_timeout=0)),
                      name="schema-swagger-ui",
                  ),
                  path("auth/", include("authorization.urls")),

                  path("banners/", include("banners.urls")),

                  path("admin/", admin.site.urls),

                  path("", include("django.contrib.auth.urls")),
                  path("dashboard/", include('dashboard.urls')),
                  path("", RedirectView.as_view(url='/admin/')),
                  # path("/", admin.site.urls),
              ]

for app in settings.APP_MODULES:
    add_module_urls(app, urlpatterns)
