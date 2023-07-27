from rest_framework import serializers
from users.serializers import AgentSerializer
from company.serializers import CompanyAgentSerializer
from users.models import Agent
from company.models import CompanyAgent
from .models import (
Country,
City, 
Property, 
Media, 
Area, 
PropertyAmenties, 
PropertyTypes, 
PropertyInstallment
)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code']

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model = City
        fields = ['id', 'country', 'city_name', 'city_code']

class AreaSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'city', 'area']

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInstallment
        fields = ['id', 'advance_amount', 'no_of_inst', 'monthly_inst', 'ready_for_possession']

class PropertyTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ['id', 'plot_types', 'home_types', 'commercial_types', 'unit_types', 'other_description']

class AmentiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenties
        fields = ['id', 'other_nearby_palces', 'bedrooms', 'distance_from_airport', 'built_in_year',
                  'bathrooms', 'kitchen', 'floors', 'maid_room', 'built_in_wardrobes', 'kitchen_appliances','balcony', 'lower_portion', 'Farmhouse', 'electricity_backup', 'furnished_unfurnished',
                  'covered_parking', 'lobby_in_building', 'security', 'parking_space', 'drawing_room', 'study_room',
                  'laundry_room', 'store_room', 'gym', 'lounge_sitting_area', 'internet', 'swimming_pool', 'mosque',
                  'kids_play_area', 'medical_center', 'community_lawn_garden', 'near_by_school', 'near_by_hospital',
                  'near_by_shopping_mall', 'other_description']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields =['image_url', 'media_type', 'created_at', 'updated_at']

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value
    
class PropertySerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True, source='property_media')
    area = AreaSerializer(read_only=True)
    amenties = AmentiesSerializer(read_only=True)
    property_types = PropertyTypesSerializer(read_only=True)
    installment = InstallmentSerializer(read_only=True)
    agent = AgentSerializer(read_only=True, required=False)
    company_agent = CompanyAgentSerializer(read_only=True, required=False)
    date = CustomDateField()

    class Meta:
        model = Property
        fields = [
            'id',
            'media',
            'R_B_type',
            'property_type',
            'area',
            'agent',
            'company_agent',
            'amenties',
            'property_types',
            'installment',
            'available',
            'date',
            'description',
            'total_price',
            'created_at',
            'updated_at',
        ]


class CreatePropertySerializer(serializers.Serializer):
    media = serializers.ListSerializer(
        child=serializers.DictField(
            child=serializers.CharField(max_length=200)
        ),
        required=True
    )
    R_B_type = serializers.ChoiceField(choices=[('rent', 'Rent'), ('buy', 'Buy')])
    property_type = serializers.CharField(max_length=100)
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all(), required=False)
    company_agent = serializers.PrimaryKeyRelatedField(queryset=CompanyAgent.objects.all(), required=False)
    amenties = serializers.PrimaryKeyRelatedField(queryset=PropertyAmenties.objects.all())
    property_types = serializers.PrimaryKeyRelatedField(queryset=PropertyTypes.objects.all())
    installment = serializers.PrimaryKeyRelatedField(queryset=PropertyInstallment.objects.all())
    available = serializers.BooleanField()
    description = serializers.CharField(max_length=1000)
    total_price = serializers.IntegerField()
    price_per_marla = serializers.IntegerField()

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        property = Property.objects.create(**validated_data)

        for media in media_data:
            Media.objects.create(property=property, **media)

        return property



