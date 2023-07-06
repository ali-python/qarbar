from rest_framework import serializers
from .models import Country, City, Property, Media, Area
from users.serializers import AgentSerializer
from company.serializers import CompanyAgentSerializer
from users.models import Agent
from company.models import CompanyAgent
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'date']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'city_name', 'city_code', 'date']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'city', 'area']

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
    agent = AgentSerializer(read_only=True)
    company_agent = CompanyAgentSerializer(read_only=True)
    date = CustomDateField()

    class Meta:
        model = Property
        fields = [
            'id',
            'media',
            'R_B_type',
            'property_type',
            'size_sqf',
            'area',
            'agent',
            'company_agent',
            'bedrooms',
            'bathrooms',
            'kitchen',
            'floors',
            'maid_room',
            'car_porch',
            'available',
            'date',
            'description',
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
    size_sqf = serializers.IntegerField()
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    company_agent = serializers.PrimaryKeyRelatedField(queryset=CompanyAgent.objects.all())
    bedrooms = serializers.IntegerField()
    bathrooms = serializers.IntegerField()
    kitchen = serializers.BooleanField()
    floors = serializers.IntegerField()
    maid_room = serializers.BooleanField()
    car_porch = serializers.BooleanField()
    available = serializers.BooleanField()
    description = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        property = Property.objects.create(**validated_data)

        for media in media_data:
            Media.objects.create(property=property, **media)

        return property



