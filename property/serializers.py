from rest_framework import serializers
from .models import Country, City, Property

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'date']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'city_name', 'city_code', 'date']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'property_type', 'size_sqf', 'city', 'agent', 'bedrooms', 'bathrooms',
                  'kitchen', 'floors', 'maid_room', 'car_porch', 'buy_rent', 'available', 'date']


