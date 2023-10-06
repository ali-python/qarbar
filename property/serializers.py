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
        fields =['image_url', 'media_type', 'created_at', 'updated_at']

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value
    
class PropertySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    media = MediaSerializer(many=True, read_only=True, source='property_media')
    area = AreaSerializer(read_only=True)
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
            'rent_sale_type',
            'area',
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
        ]
    def get_agent(self, obj):
        agent = obj.agent
        if agent is not None:
            return AgentSerializer(agent).data
        else:
            return None
    
    
    # def watermark_image(self, image_url):
    #         # Fetch the original image
    #         try:
    #             media_response = requests.get(image_url)
    #             media_response.raise_for_status()  # Raise an exception for non-200 status codes
    #             media_bytes = BytesIO(media_response.content)
    #             image = Image.open(media_bytes)
    #         except requests.exceptions.RequestException as e:
    #             raise Exception(f"Failed to download media image from URL: {e}")
    #         except UnidentifiedImageError:
    #             raise Exception("Invalid image format")

    #         # Fetch the watermark image
    #         watermark_url = 'https://meditech-products.s3-ap-northeast-1.amazonaws.com/WhatsApp%20Image%202023-09-15%20at%203.00.29%20PM.jpeg'  # Replace with your watermark image URL
    #         try:
    #             watermark_response = requests.get(watermark_url)
    #             watermark_response.raise_for_status()  # Raise an exception for non-200 status codes
    #             watermark_bytes = BytesIO(watermark_response.content)
    #             watermark = Image.open(watermark_bytes)
    #         except requests.exceptions.RequestException as e:
    #             raise Exception(f"Failed to download watermark image from URL: {e}")
    #         except UnidentifiedImageError:
    #             raise Exception("Invalid watermark image format")

    #         # Ensure both images have the same transparency mode (RGBA)
    #         if image.mode != "RGBA":
    #             image = image.convert("RGBA")
    #         if watermark.mode != "RGBA":
    #             watermark = watermark.convert("RGBA")

    #         # Resize the watermark to fit the image
    #         width, height = image.size
    #         watermark = watermark.resize((int(width * 0.2), int(height * 0.2)))

    #         # Paste the watermark on the image
    #         image.paste(watermark, (width - watermark.width, height - watermark.height), watermark)

    #         return image

    # def to_representation(self, instance):
    #     # Serialize the instance as usual
    #     data = super().to_representation(instance)

    #     # Check if there are media items
    #     if 'media' in data and data['media']:
    #         # Iterate over the media items and watermark the images
    #         for media_item in data['media']:
    #             image_url = media_item.get('image_url')
    #             if image_url:
    #                 try:
    #                     # Call watermark_image method to get the watermarked image
    #                     watermarked_image = self.watermark_image(image_url)

    #                     # Convert the watermarked image to base64
    #                     buffered = BytesIO()
    #                     watermarked_image.save(buffered, format="PNG")
    #                     base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Convert to base64 and decode

    #                     # Add the base64 watermarked image to the media item
    #                     media_item['watermarked_image'] = base64_image
    #                 except Exception as e:
    #                     # Handle any exceptions that may occur during image processing
    #                     media_item['watermarked_image_error'] = str(e)

    #     return data


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

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        media_data = validated_data.pop('media')
        amenties_data = validated_data.pop('amenties', None)
        property_type_data = validated_data.pop('property_type', None)
        property_location_data = validated_data.pop('property_location', None)
        installment_data = validated_data.pop('installment', None)

        property = Property.objects.create(**validated_data)
        if amenties_data:
            pa=PropertyAmenties.objects.create(property=property, **amenties_data)
            property.amenties=pa
            property.save()
        if property_type_data:
            pt=PropertyTypes.objects.create(property=property, **property_type_data)
            property.property_type=pt
            property.save()
        if property_location_data:
            pl=PropertyLocation.objects.create(property=property, **property_location_data)
            property.property_location=pl
            property.save()
        if installment_data:
            pi=PropertyInstallment.objects.create(property=property, **installment_data)
            property.installment=pi
            property.save()
        for media in media_data:
            Media.objects.create(property=property, **media)

            return property

    #     # Watermark and save each image to the Media model
    #     for media in media_data:
    #         image_url = media.get('image_url')
    #         if image_url:
    #             image_with_watermark = self.add_watermark(image_url)

    #             # Create a Media instance with the watermarked image
    #             media_instance = Media(property=property, media_type='image', image_url=image_url)
    #             media_instance.save()

    #     return property

    # def add_watermark(self, image_url):
    #     # Open the media image
    #     media_response = requests.get(image_url)

    #     if media_response.status_code == 200:
    #         media_bytes = BytesIO(media_response.content)
    #         image = Image.open(media_bytes)

    #         # Open the watermark image
    #         watermark_url = 'https://meditech-products.s3-ap-northeast-1.amazonaws.com/WhatsApp%20Image%202023-09-15%20at%203.00.29%20PM.jpeg'  # Replace with your watermark image URL
    #         watermark_response = requests.get(watermark_url)

    #         if watermark_response.status_code == 200:
    #             watermark_bytes = BytesIO(watermark_response.content)
    #             watermark = Image.open(watermark_bytes)

    #             # Ensure both images have the same transparency mode (RGBA)
    #             if image.mode != "RGBA":
    #                 image = image.convert("RGBA")

    #             # Resize the watermark image to fit the image
    #             width, height = image.size
    #             watermark = watermark.resize((int(width * 0.2), int(height * 0.2)))

    #             # Create a transparent layer for the watermark
    #             watermark_layer = Image.new("RGBA", image.size)
    #             watermark_layer.paste(watermark, (width - watermark.width, height - watermark.height), watermark)

    #             # Composite the watermark onto the original image
    #             watermarked_image = Image.alpha_composite(image, watermark_layer)

    #             return watermarked_image

    #     raise Exception("Failed to add watermark to the image")
    
    # def save_watermarked_image(self, watermarked_image, original_image_name):
    #     # Convert the watermarked image to RGB mode (removing the alpha channel)
    #     watermarked_image = watermarked_image.convert("RGB")

    #     buffer = BytesIO()
    #     watermarked_image.save(buffer, format='JPEG')
    #     return InMemoryUploadedFile(buffer, None, original_image_name, 'image/jpeg', buffer.tell(), None)

    # def get_image_name(self, image_url):
    #     # Extract the image name from the URL
    #     return image_url.split('/')[-1]

