import django_filters
from django_filters import rest_framework as filters
from .models import Projects

class ProjectFilter(filters.FilterSet):
    project_types = django_filters.ChoiceFilter(choices=Projects.PROJECT_TYPES)
    plot_types = django_filters.CharFilter(field_name='property_type__plot_types', lookup_expr='icontains')
    home_types = django_filters.CharFilter(field_name='property_type__home_types', lookup_expr='icontains')
    commercial_types = django_filters.CharFilter(field_name='property_type__commercial_types', lookup_expr='icontains')
    beds = filters.AllValuesMultipleFilter(field_name='amenities__bedrooms')
    title = django_filters.CharFilter(lookup_expr='icontains')
    total_price = django_filters.NumberFilter(lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    cities = filters.AllValuesMultipleFilter(field_name='city__city_name')
    countries = filters.AllValuesMultipleFilter(field_name='country__country_name')

    class Meta:
        model = Projects    
        fields = {}

    