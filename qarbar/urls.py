"""
URL configuration for qarbar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from property.views import CountryViewSet, CityViewSet, PropertyViewSet, AreaViewSet
from users.views import LoginView, RegisterView, UserViewSet, AgentViewSet
from company.views import CompanyViewSet, CustomUserViewSet, CompanyAgentViewSet
from news.views import NewsViewSet
from new_projects.views import ProjectViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
router = routers.DefaultRouter()
router.register(r'api/v1/user', UserViewSet, basename='user')
router.register(r'api/v1/agent', AgentViewSet, basename='agent')
router.register(r'api/v1/countries', CountryViewSet, basename='country')
router.register(r'api/v1/cities', CityViewSet, basename='city')
router.register(r'api/v1/area', AreaViewSet, basename='area')
router.register(r'api/v1/properties', PropertyViewSet, basename='property')
router.register(r'api/v1/companies', CompanyViewSet, basename='company')
router.register(r'api/v1/custom/company/users', CustomUserViewSet, basename='customuserscompany')
router.register(r'api/v1/company/agents', CompanyAgentViewSet, basename='agents_company')
router.register(r'api/v1/news', NewsViewSet, basename='news')
router.register(r'api/v1/new/projects', ProjectViewSet, basename='projects')

schema_view = get_schema_view(
    openapi.Info(
        title="QARBAR",
        default_version="v1",
        description="Qarbar API's ",
        terms_of_service="http://13.127.231.16/",
        contact=openapi.Contact(email="aliakber419@gmail.com"),
        license=openapi.License(name="Qarbar License"),
    ),
    public=True,
    permission_classes=(),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path('api/v1/auth/login/', LoginView.as_view(), name="login_api"),
    path('api/v1/auth/register/', RegisterView.as_view(), name="register_api"),
    # path('api/v1/auth/register/agent-list/', AgentView.as_view(), name="register_api")
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

