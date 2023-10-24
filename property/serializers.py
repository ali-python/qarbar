from rest_framework import serializers
from rest_framework.fields import SkipField
from users.serializers import AgentSerializer
from company.serializers import CompanyAgentSerializer
from users.models import Agent
from company.models import CompanyAgent
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse 
from users.serializers import UserSerializer
from io import BytesIO
from django.contrib.auth.models import User
import base64
import requests
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
        allow_null = True

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields =['id', 'image_url', 'media_type', 'created_at', 'updated_at']

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value
    
class PropertySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    media = MediaSerializer(many=True, read_only=True, source='property_media')
    amenties = AmentiesSerializer(read_only=True, allow_null = True)
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
            'phone',
            'landline',
            'secondry_phone',
            'email',
            'rent_sale_type',
            'user',
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
            'views_count',
            'created_at',
            'updated_at',
            'admin_check'
        ]
    def get_agent(self, obj):
        agent = obj.agent
        if agent is not None:
            return AgentSerializer(agent).data
        else:
            return None
    

# class CreatePropertySerializer(serializers.ModelSerializer):
#     media = serializers.ListSerializer(
#         child=serializers.DictField(
#             child=serializers.CharField(max_length=200)
#         ),
#         required=True
#     )
#     amenties = AmentiesSerializer(allow_null=True, required=False)
#     property_type = PropertyTypesSerializer(allow_null=True, required=False)
#     property_location = PropertyLocationSerializer(allow_null=True, required=False)
#     installment = InstallmentSerializer(allow_null=True, required=False)
#     user = UserSerializer(allow_null=True, required=False)
#     agent = AgentSerializer(allow_null=True, required=False)
#     company_agent = CompanyAgentSerializer(allow_null=True, required=False)

#     class Meta:
#         model = Property
#         fields = '__all__'

    # def create(self, validated_data):
    #     media_data = validated_data.pop('media')
    #     amenties_data = validated_data.pop('amenties', None)
    #     property_type_data = validated_data.pop('property_type', None)
    #     property_location_data = validated_data.pop('property_location', None)
    #     installment_data = validated_data.pop('installment', None)
    #     user_data = validated_data.pop('user', None)
    #     agent_data = validated_data.pop('agent', None)
    #     company_agent_data = validated_data.pop('company_agent', None)

    #     if agent_data and 'user' in agent_data:
    #         agent_data.pop('user')
            
    #     property = Property.objects.create(**validated_data)

    #     # Create related objects and link them to the property
    #     if amenties_data:
    #         pa = PropertyAmenties.objects.create(property=property, **amenties_data)
    #         property.amenties = pa
    #         property.save()

    #     if property_type_data:
    #         pt = PropertyTypes.objects.create(property=property, **property_type_data)
    #         property.property_type = pt
    #         property.save()

    #     if property_location_data:
    #         pl = PropertyLocation.objects.create(property=property, **property_location_data)
    #         property.property_location = pl
    #         property.save()

    #     if installment_data:
    #         pi = PropertyInstallment.objects.create(property=property, **installment_data)
    #         property.installment = pi
    #         property.save()

    #     if user_data:
    #         user = User.objects.create(**user_data)
    #         property.user = user
    #         property.save()

    #     if agent_data:
    #         agent = Agent.objects.create(**agent_data)
    #         property.agent = agent
    #         property.save()

    #     if company_agent_data:
    #         company_agent = CompanyAgent.objects.create(**company_agent_data)
    #         property.company_agent = company_agent
    #         property.save()

    #     for media in media_data:
    #         Media.objects.create(property=property, **media)

    #     return property

# class CreatePropertySerializer(serializers.ModelSerializer):
#     media = serializers.ListSerializer(
#         child=serializers.DictField(
#             child=serializers.CharField(max_length=200)
#         ),
#         required=True
#     )
#     amenties = AmentiesSerializer(allow_null=True, required=False)
#     property_type = PropertyTypesSerializer(allow_null=True, required=False)
#     property_location = PropertyLocationSerializer(allow_null=True, required=False)
#     installment = InstallmentSerializer(allow_null=True, required=False)
#     agent_id = serializers.IntegerField(allow_null=True, required=False)

#     class Meta:
#         model = Property
#         exclude = ('user', 'agent', 'company_agent')

#     def create(self, validated_data):
#         media_data = validated_data.pop('media')
#         amenties_data = validated_data.pop('amenties', None)
#         property_type_data = validated_data.pop('property_type', None)
#         property_location_data = validated_data.pop('property_location', None)
#         installment_data = validated_data.pop('installment', None)
#         agent_id = validated_data.pop('agent_id', None)

#         # Create the property
#         property = Property.objects.create(**validated_data)

#         # Link the agent (if agent_id is provided)
#         if agent_id:
#             try:
#                 agent = Agent.objects.get(id=agent_id)
#                 property.agent = agent
#                 property.save()
#             except Agent.DoesNotExist:
#                 pass  # Handle the case where the provided agent ID does not exist

#         # Create related objects and link them to the property
#         if amenties_data:
#             pa = PropertyAmenties.objects.create(property=property, **amenties_data)
#             property.amenties = pa
#             property.save()

#         if property_type_data:
#             pt = PropertyTypes.objects.create(property=property, **property_type_data)
#             property.property_type = pt
#             property.save()

#         if property_location_data:
#             pl = PropertyLocation.objects.create(property=property, **property_location_data)
#             property.property_location = pl
#             property.save()

#         if installment_data:
#             pi = PropertyInstallment.objects.create(property=property, **installment_data)
#             property.installment = pi
#             property.save()

#         for media in media_data:
#             Media.objects.create(property=property, **media)

#         return property

class CreatePropertySerializer(serializers.ModelSerializer):
    media = serializers.ListSerializer(
        child=serializers.DictField(
            child=serializers.CharField(max_length=200)
        ),
        required=True
    )
    amenties = AmentiesSerializer(allow_null=True, required=False)
    property_type = PropertyTypesSerializer(allow_null=True, required=False)
    property_location = PropertyLocationSerializer(allow_null=True, required=False)
    installment = InstallmentSerializer(allow_null=True, required=False)
    agent_id = serializers.IntegerField(allow_null=True, required=False)
    user_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Property
        exclude = ('user', 'agent', 'company_agent')

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        amenties_data = validated_data.pop('amenties', None)
        property_type_data = validated_data.pop('property_type', None)
        property_location_data = validated_data.pop('property_location', None)
        installment_data = validated_data.pop('installment', None)
        agent_id = validated_data.pop('agent_id', None)
        user_id = validated_data.pop('user_id', None)

        # Create the property
        property = Property.objects.create(**validated_data)

        # Link the agent (if agent_id is provided)
        if agent_id:
            try:
                agent = Agent.objects.get(id=agent_id)
                property.agent = agent
                property.save()
            except Agent.DoesNotExist:
                pass  # Handle the case where the provided agent ID does not exist

        # Link the user (if user_id is provided)
        if user_id:
            print(user_id)
            print("_________________________")
            try:
                user = User.objects.get(id=user_id)
                property.user = user
                property.save()
            except User.DoesNotExist:
                pass  # Handle the case where the provided user ID does not exist

        # Create related objects and link them to the property
        if amenties_data:
            pa = PropertyAmenties.objects.create(property=property, **amenties_data)
            property.amenties = pa
            property.save()

        if property_type_data:
            pt = PropertyTypes.objects.create(property=property, **property_type_data)
            property.property_type = pt
            property.save()

        if property_location_data:
            pl = PropertyLocation.objects.create(property=property, **property_location_data)
            property.property_location = pl
            property.save()

        if installment_data:
            pi = PropertyInstallment.objects.create(property=property, **installment_data)
            property.installment = pi
            property.save()

        for media in media_data:
            Media.objects.create(property=property, **media)

        return property
