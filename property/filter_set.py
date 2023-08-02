import django_filters
from django_filters import rest_framework as filters
from .models import Property
from .serializers import PropertySerializer

# class PropertyFilter(django_filters.FilterSet):
#     area = django_filters.CharFilter(field_name='area__name', lookup_expr='icontains')
#     city_name = django_filters.CharFilter(field_name='area__city__city_name', lookup_expr='icontains')
#     available = django_filters.BooleanFilter()
#     agent = django_filters.CharFilter(field_name='agent__name', lookup_expr='icontains')
#     R_S_type = django_filters.ChoiceFilter(choices=Property.R_S_TYPES)
#     property_types = django_filters.CharFilter(field_name='property_type', lookup_expr='icontains')
#     size_sqf = django_filters.NumberFilter(field_name='size_sqf', lookup_expr='exact')
#     total_price = django_filters.NumberFilter(field_name='total_price', lookup_expr='exact')
#     maid_room = django_filters.BooleanFilter()

#     class Meta:
#         model = Property
#         fields = [
#                 'area',
#                 'property_types', 
#                 'total_price', 
#                 'city_name', 
#                 'available', 
#                 'agent', 
#                 'R_S_type', 
#                 'size_sqf', 
#                 'maid_room'
#                 ]

class PropertyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    rent_sale_type = django_filters.ChoiceFilter(choices=Property.R_S_TYPES)
    area__name = django_filters.CharFilter(lookup_expr='icontains')
    agent__name = django_filters.CharFilter(lookup_expr='icontains')
    company_agent__name = django_filters.CharFilter(lookup_expr='icontains')
    amenties__bedrooms = django_filters.NumberFilter(lookup_expr='exact')
    amenties__distance_from_airport = django_filters.NumberFilter(lookup_expr='exact')
    amenties__built_in_year = django_filters.NumberFilter(lookup_expr='exact')
    amenties__bathrooms = django_filters.NumberFilter(lookup_expr='exact')
    amenties__kitchen = django_filters.NumberFilter(lookup_expr='exact')
    amenties__floors = django_filters.NumberFilter(lookup_expr='exact')
    amenties__maid_room = django_filters.BooleanFilter()
    amenties__built_in_wardrobes = django_filters.BooleanFilter()
    amenties__kitchen_appliances = django_filters.BooleanFilter()
    amenties__balcony = django_filters.BooleanFilter()
    amenties__lower_portion = django_filters.BooleanFilter()
    amenties__Farmhouse = django_filters.BooleanFilter()
    amenties__electricity_backup = django_filters.BooleanFilter()
    amenties__furnished_unfurnished = django_filters.BooleanFilter()
    amenties__covered_parking = django_filters.BooleanFilter()
    amenties__lobby_in_building = django_filters.BooleanFilter()
    amenties__security = django_filters.BooleanFilter()
    amenties__parking_space = django_filters.BooleanFilter()
    amenties__drawing_room = django_filters.BooleanFilter()
    amenties__study_room = django_filters.BooleanFilter()
    amenties__laundry_room = django_filters.BooleanFilter()
    amenties__store_room = django_filters.BooleanFilter()
    amenties__gym = django_filters.BooleanFilter()
    amenties__lounge_sitting_area = django_filters.BooleanFilter()
    amenties__internet = django_filters.BooleanFilter()
    amenties__swimming_pool = django_filters.BooleanFilter()
    amenties__mosque = django_filters.BooleanFilter()
    amenties__kids_play_area = django_filters.BooleanFilter()
    amenties__medical_center = django_filters.BooleanFilter()
    amenties__community_lawn_garden = django_filters.BooleanFilter()
    amenties__near_by_school = django_filters.BooleanFilter()
    amenties__near_by_hospital = django_filters.BooleanFilter()
    amenties__near_by_shopping_mall = django_filters.BooleanFilter()
    amenties__other_description = django_filters.CharFilter(lookup_expr='icontains')
    property_type__plot_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__home_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__commercial_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__unit_types = django_filters.CharFilter(lookup_expr='icontains')
    property_type__size_sqf = django_filters.NumberFilter(lookup_expr='exact')
    property_type__other_description = django_filters.CharFilter(lookup_expr='icontains')
    property_location__latitude = django_filters.NumberFilter(lookup_expr='exact')
    property_location__longitude = django_filters.NumberFilter(lookup_expr='exact')
    installment__advance_amount = django_filters.NumberFilter(lookup_expr='exact')
    installment__no_of_inst = django_filters.NumberFilter(lookup_expr='exact')
    installment__monthly_inst = django_filters.NumberFilter(lookup_expr='exact')
    installment__ready_for_possession = django_filters.BooleanFilter()
    available = django_filters.BooleanFilter()
    description = django_filters.CharFilter(lookup_expr='icontains')
    total_price = django_filters.NumberFilter(lookup_expr='exact')
    date = django_filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Property
        fields = []


