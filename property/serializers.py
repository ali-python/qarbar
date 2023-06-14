from rest_framework import serializers
from .models import Country, City, Property, Media
from users.serializers import AgentSerializer
from users.models import Agent

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_code', 'date']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'city_name', 'city_code', 'date']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields =['image_url', 'media_type', 'created_at', 'updated_at']

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        # Convert the datetime value to a date value
        return value.date()
    
class PropertySerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True, source='property_media')
    city = CitySerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    date = CustomDateField()  # Use the custom date field for the 'date' field

    class Meta:
        model = Property
        fields = [
            'id',
            'media',
            'R_B_type',
            'property_type',
            'size_sqf',
            'city',
            'agent',
            'bedrooms',
            'bathrooms',
            'kitchen',
            'floors',
            'maid_room',
            'car_porch',
            'available',
            'address_area',
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
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    bedrooms = serializers.IntegerField()
    bathrooms = serializers.IntegerField()
    kitchen = serializers.BooleanField()
    floors = serializers.IntegerField()
    maid_room = serializers.BooleanField()
    car_porch = serializers.BooleanField()
    available = serializers.BooleanField()
    description = serializers.CharField(max_length=1000)
    address_area = serializers.CharField(max_length=200)

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        property = Property.objects.create(**validated_data)

        for media in media_data:
            Media.objects.create(property=property, **media)

        return property



