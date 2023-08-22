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
from django.urls import path, include
from rest_framework import routers
from property.views import CountryViewSet, CityViewSet, PropertyViewSet, AreaViewSet
from users.views import LoginView, RegisterView, UserViewSet, AgentViewSet
from company.views import CompanyViewSet, CustomUserViewSet, CompanyAgentViewSet
from new_projects.views import ProjectViewSet
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
router.register(r'api/v1/new/projects', ProjectViewSet, basename='projects')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path('api/v1/auth/login/', LoginView.as_view(), name="login_api"),
    path('api/v1/auth/register/', RegisterView.as_view(), name="register_api"),
    # path('api/v1/auth/register/agent-list/', AgentView.as_view(), name="register_api")
]

