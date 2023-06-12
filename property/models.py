from django.db import models
from users .models import Agent
from django.utils import timezone


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.country_name
    
class City(models.Model):
    country = models.ForeignKey(Country, related_name="country_city", on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.city_name

class Property(models.Model):
    PROPERTY_TYPES = (
        ('villa', 'Villa'),
        ('house', 'House'),
        ('land', 'Land'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial'),
    )

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default="villa")
    size_sqf = models.IntegerField(default=0)
    city = models.ForeignKey(City, related_name="property_city", on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, related_name="property_agent", on_delete=models.CASCADE)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    kitchen = models.BooleanField()
    floors = models.IntegerField()
    maid_room = models.BooleanField()
    car_porch = models.BooleanField()
    buy_rent = models.BooleanField()
    available = models.BooleanField(default=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.property_type} in {self.city.city_name}"