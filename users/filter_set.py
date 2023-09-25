import django_filters
from django_filters import rest_framework as filters
from .models import Agent

class AgentFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    nationality = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    province = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Agent    
        fields = {}