import django_filters
from django_filters import rest_framework as filters
from .models import Property
from .serializers import PropertySerializer

class PropertyFilter(django_filters.FilterSet):
    area = django_filters.CharFilter(field_name='area__name', lookup_expr='icontains')
    city_name = django_filters.CharFilter(field_name='area__city__city_name', lookup_expr='icontains')
    available = django_filters.BooleanFilter()
    agent = django_filters.CharFilter(field_name='agent__name', lookup_expr='icontains')
    R_B_type = django_filters.ChoiceFilter(choices=Property.R_B_TYPES)
    property_types = django_filters.CharFilter(field_name='property_type', lookup_expr='icontains')
    size_sqf = django_filters.NumberFilter(field_name='size_sqf', lookup_expr='exact')
    total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='exact')
    maid_room = django_filters.BooleanFilter()

    class Meta:
        model = Property
        fields = ['area','property_types', 'total_price', 'city_name', 'available', 'agent', 'R_B_type', 'size_sqf', 'maid_room']

