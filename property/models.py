from django.db import models
from users .models import Agent
from django.utils import timezone
from core.models import DatedModel
from company.models import CompanyAgent

class Country(DatedModel):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.country_name
    
class City(DatedModel):
    country = models.ForeignKey(Country, related_name="country_city", on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.city_name
    
class Area(DatedModel):
    city=models.ForeignKey(City, related_name="city_area", on_delete=models.CASCADE, null=True, blank=True)
    area = models.CharField(max_length=200)

    def __str__(self):
        return self.city.city_name

class Property(DatedModel):
    PROPERTY_TYPES = (
        ('plot', 'Plot'),
        ('villa', 'Villa'),
        ('house', 'House'),
        ('land', 'Land'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial')
    )
    R_B_TYPES = (
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    )
    R_B_type = models.CharField(max_length=20, choices=R_B_TYPES, default="rent")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default="villa")
    size_sqf = models.IntegerField(default=0)
    area = models.ForeignKey(Area, related_name="property_area", on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(Agent, related_name="individual_properties", on_delete=models.CASCADE, null=True, blank=True)
    company_agent = models.ForeignKey(CompanyAgent, related_name="company_properties", on_delete=models.CASCADE, null=True, blank=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    kitchen = models.BooleanField()
    floors = models.IntegerField()
    maid_room = models.BooleanField()
    car_porch = models.BooleanField()
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.property_type}"

class PropertyLocation(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"Location for Property: {self.property}"
    
class Media(DatedModel):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('Video', 'Video'),
    )
    property = models.ForeignKey(Property, related_name="property_media", on_delete=models.CASCADE, null=True, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default="image")
    image_url = models.CharField(max_length=250)
    
    def __str__(self):
        return self.media_type