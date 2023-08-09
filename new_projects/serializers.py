from rest_framework import serializers
from .models import PorjectAmenities, UnitType, ProjectBed, Document, Projects, Media
from property.models import PropertyTypes, PropertyLocation, PropertyInstallment, City, Country
from property. serializers import AgentSerializer, CompanyAgentSerializer
from property.serializers import (
    PropertyTypesSerializer, 
    PropertyLocationSerializer, 
    InstallmentSerializer
    )

class PorjectAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorjectAmenities
        fields = '__all__'

class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'

class ProjectBedSerializer(serializers.ModelSerializer):
    unit_type = UnitTypeSerializer()

    class Meta:
        model = ProjectBed
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    brochure_document = DocumentSerializer()
    available_units = ProjectBedSerializer()
    amenities = PorjectAmenitiesSerializer()
    agent = AgentSerializer()
    company_agent = CompanyAgentSerializer()

    class Meta:
        model = Projects
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    new_project = ProjectsSerializer()

    class Meta:
        model = Media
        fields = '__all__'

class CreateProjectSerializer(serializers.ModelSerializer):
    media = serializers.ListSerializer(
        child=serializers.DictField(
            child=serializers.CharField(max_length=200)
        ),
        required=True
    )
    amenities = PorjectAmenitiesSerializer()
    property_type = PropertyTypesSerializer()
    property_location = PropertyLocationSerializer()
    installment = InstallmentSerializer()

    available_units = serializers.ListSerializer(
        child=ProjectBedSerializer(),
        required=False
    )

    class Meta:
        model = Projects
        fields = '__all__'

    def create(self, validated_data):
        media_data = validated_data.pop('media')

        amenities_data = validated_data.pop('amenities', None)
        property_type_data = validated_data.pop('property_type', None)
        property_location_data = validated_data.pop('property_location', None)
        installment_data = validated_data.pop('installment', None)

        available_units_data = validated_data.pop('available_units', [])

        project = Projects.objects.create(**validated_data)

        for unit_data in available_units_data:
            unit_type_data = unit_data.pop('unit_type')
            unit_type, created = UnitType.objects.get_or_create(**unit_type_data)
            
            project_bed = ProjectBed.objects.create(unit_type=unit_type, **unit_data)
            project.available_units = project_bed

        if amenities_data:
            amenities_instance = PorjectAmenities.objects.create(**amenities_data)
            project.amenities = amenities_instance

        if property_type_data:
            property_type_instance = PropertyTypes.objects.create(**property_type_data)
            project.property_type = property_type_instance

        if property_location_data:
            property_location_instance = PropertyLocation.objects.create(**property_location_data)
            project.property_location = property_location_instance

        if installment_data:
            installment_instance = PropertyInstallment.objects.create(**installment_data)
            project.installment = installment_instance

        for media in media_data:
            Media.objects.create(project=project, **media)

        return project
