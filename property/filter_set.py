import django_filters
from django_filters import rest_framework as filters
from .models import Property
    
class PropertyFilter(filters.FilterSet):
    beds = filters.AllValuesMultipleFilter(field_name='amenties__bedrooms')
    baths = filters.AllValuesMultipleFilter(field_name='amenties__bathrooms')
    cities = filters.AllValuesMultipleFilter(field_name='property_location__city_area')
    countries = filters.AllValuesMultipleFilter(field_name='property_location__city_area')
    title = django_filters.CharFilter(lookup_expr='icontains')
    total_price = django_filters.NumberFilter(lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    size = django_filters.NumberFilter(lookup_expr='exact')
    min_size = django_filters.NumberFilter(field_name='property_type__size', lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name='property_type__size', lookup_expr='lte')
    rent_sale_type = django_filters.ChoiceFilter(choices=Property.R_S_TYPES)
    agent__name = django_filters.CharFilter(lookup_expr='icontains')
    company_agent__name = django_filters.CharFilter(lookup_expr='icontains')
    plot_types = django_filters.CharFilter(field_name='property_type__plot_types', lookup_expr='icontains')
    home_types = django_filters.CharFilter(field_name='property_type__home_types', lookup_expr='icontains')
    commercial_types = django_filters.CharFilter(field_name='property_type__commercial_types', lookup_expr='icontains')
    unit_type = django_filters.CharFilter(field_name='property_type__unit_types', lookup_expr='icontains')
    class Meta:
        model = Property
        fields = {}



