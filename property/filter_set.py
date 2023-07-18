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
    bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='exact')
    size_sqf = django_filters.NumberFilter(field_name='size_sqf', lookup_expr='exact')
    price_per_marla = django_filters.NumberFilter(field_name='size_sqf', lookup_expr='exact')
    size_sqf = django_filters.NumberFilter(field_name='size_sqf', lookup_expr='exact')
    maid_room = django_filters.BooleanFilter()

    class Meta:
        model = Property
        fields = ['area','price_per_marla', 'city_name', 'available', 'agent', 'R_B_type', 'bedrooms', 'size_sqf', 'maid_room']

