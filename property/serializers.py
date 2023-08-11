from rest_framework import serializers
from rest_framework.fields import SkipField
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
    PropertyInstallment,
    PropertyLocation
    )
class PropertyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyLocation
        fields = '__all__'

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
        fields = ['id', 'plot_types', 'home_types', 'commercial_types', 'unit_types', 'size', 'other_description']

class AmentiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenties
        fields = '__all__'

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
    property_location = PropertyLocationSerializer(read_only=True)
    property_type = PropertyTypesSerializer(read_only=True)
    installment = InstallmentSerializer(read_only=True)
    agent = AgentSerializer(read_only=True, required=False)
    company_agent = CompanyAgentSerializer(read_only=True, required=False)
    date = CustomDateField()

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'media',
            'rent_sale_type',
            'area',
            'agent',
            'company_agent',
            'amenties',
            'property_location',
            'property_type',
            'installment',
            'available',
            'date',
            'description',
            'total_price',
            'created_at',
            'updated_at',
        ]
    def get_agent(self, obj):
        agent = obj.agent
        if agent is not None:
            return AgentSerializer(agent).data
        else:
            return None

class CreatePropertySerializer(serializers.ModelSerializer):
    media = serializers.ListSerializer(
        child=serializers.DictField(
            child=serializers.CharField(max_length=200)
        ),
        required=True
    )
    amenties = AmentiesSerializer()
    property_type = PropertyTypesSerializer()
    property_location = PropertyLocationSerializer()
    installment = InstallmentSerializer()

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        media_data = validated_data.pop('media')

        # Create related models first and then assign them to the main instance
        amenties_data = validated_data.pop('amenties', None)
        property_type_data = validated_data.pop('property_type', None)
        property_location_data = validated_data.pop('property_location', None)
        installment_data = validated_data.pop('installment', None)

        property = Property.objects.create(**validated_data)

        # Handle nested objects
        if amenties_data:
            PropertyAmenties.objects.create(property=property, **amenties_data)
        if property_type_data:
            PropertyTypes.objects.create(property=property, **property_type_data)
        if property_location_data:
            PropertyLocation.objects.create(property=property, **property_location_data)
        if installment_data:
            PropertyInstallment.objects.create(property=property, **installment_data)

        for media in media_data:
            Media.objects.create(property=property, **media)

        return property

