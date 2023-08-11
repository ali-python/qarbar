import django_filters
from django_filters import rest_framework as filters
from .models import Property
    
class PropertyFilter(filters.FilterSet):
    amenties__bedrooms = filters.AllValuesMultipleFilter(field_name='amenties__bedrooms')
    amenties__bathrooms = filters.AllValuesMultipleFilter(field_name='amenties__bathrooms')
    area__city__city_name = django_filters.CharFilter(lookup_expr='icontains')
    area__city__country__country_name = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    total_price = django_filters.NumberFilter(lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    property_type__size_sqf = django_filters.NumberFilter(lookup_expr='exact')
    min_size = django_filters.NumberFilter(field_name='property_type__size_sqf', lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name='property_type__size_sqf', lookup_expr='lte')
    rent_sale_type = django_filters.ChoiceFilter(choices=Property.R_S_TYPES)
    agent__name = django_filters.CharFilter(lookup_expr='icontains')
    company_agent__name = django_filters.CharFilter(lookup_expr='icontains')
    property_type__plot_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__home_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__commercial_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__unit_types = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Property
        fields = {}



