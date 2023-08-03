from django.db import models
from users .models import Agent
from django.utils import timezone
from core.models import DatedModel
from company.models import CompanyAgent

class Country(DatedModel):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name
    
class City(DatedModel):
    country = models.ForeignKey(Country, related_name="country_city", on_delete=models.CASCADE, null=True, blank=True)
    city_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=10)

    def __str__(self):
        return self.city_name
    
class Area(DatedModel):
    city=models.ForeignKey(City, related_name="city_area", on_delete=models.CASCADE, null=True, blank=True)
    area = models.CharField(max_length=200)

    def __str__(self):
        if self.city:
            return f"{self.city} - {self.area}"
        return self.area

class PropertyAmenties(models.Model):
    other_nearby_palces = models.CharField(max_length=250)
    bedrooms = models.IntegerField(default=1)
    distance_from_airport = models.IntegerField(null=True)
    built_in_year = models.IntegerField(null=True)
    bathrooms = models.IntegerField(default=1)
    kitchen = models.IntegerField(default=0)
    floors = models.IntegerField(default=0)
    maid_room = models.BooleanField(default=False)
    built_in_wardrobes = models.BooleanField(default=False)
    kitchen_appliances = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    lower_portion = models.BooleanField(default=False)
    Farmhouse = models.BooleanField(default=False)
    electricity_backup = models.BooleanField(default=False)
    furnished_unfurnished = models.BooleanField(default=False)
    covered_parking = models.BooleanField(default=False)
    lobby_in_building = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    parking_space = models.BooleanField(default=False)
    drawing_room = models.BooleanField(default=False)
    study_room = models.BooleanField(default=False)
    laundry_room = models.BooleanField(default=False)
    store_room = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    lounge_sitting_area = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    mosque = models.BooleanField(default=False)
    kids_play_area = models.BooleanField(default=False)
    medical_center = models.BooleanField(default=False)
    community_lawn_garden = models.BooleanField(default=False)
    near_by_school = models.BooleanField(default=False)
    near_by_hospital = models.BooleanField(default=False)
    near_by_shopping_mall = models.BooleanField(default=False) 
    other_description = models.CharField(max_length=350)

    def __str__(self):
        return f"{self.built_in_year}"

class PropertyTypes(models.Model):
    HOME_TYPES = (
        ('house', 'House'),
        ('flat', 'Flat'),
        ('upper_portion', 'Uper Portion'),
        ('lower_portion', 'Lower Portion'),
        ('farm_house', 'Farm House'),
        ('room', 'Room'),
        ('pent_house', 'Pent House'),
    )
    PLOT_TYPES = (
        ('residetial_plot', 'Residential Plot'),
        ('commercial_plot', 'Commercial Plot'),
        ('agricultural_land', 'Agricultural Land'),
        ('Industrial_land', 'Industrial_Land'),
        ('plot_file', 'Plot File'),
        ('plot_form', 'Plot Form'),
    )
    COMMERCIAL_TYPES = (
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('warehouse', 'WareHouse'),
        ('factory', 'Factory'),
        ('building', 'Building'),
        ('other', 'other'),
    )
    UNIT_TYPES = (
        ('marla', 'Marla'),
        ('sqft', 'Sq.Ft.'),
        ('sqm', 'Sq.M.'),
        ('sqyd', 'Sq.Yd.'),
        ('kanal', 'Kanal'),
    )
    plot_types = models.CharField(max_length=100, choices=PLOT_TYPES, default="residetial_plot", null=True, blank=True)
    home_types = models.CharField(max_length=100, choices=HOME_TYPES, default="house", null=True, blank=True)
    commercial_types = models.CharField(max_length=100, choices=COMMERCIAL_TYPES, default="office", null=True, blank=True)
    unit_types = models.CharField(max_length=100, choices=UNIT_TYPES, default="marla", null=True, blank=True)
    size_sqf = models.IntegerField(default=0, null=True, blank=True)
    other_description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.unit_types}"

class PropertyInstallment(models.Model):
    advance_amount = models.IntegerField(default=0)
    no_of_inst = models.IntegerField(default=1)
    monthly_inst = models.IntegerField(default=0)
    ready_for_possession = models.BooleanField(default=False)

class PropertyLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

class Property(DatedModel):
    R_S_TYPES = (
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, default=0)
    landline = models.CharField(max_length=50, null=True, blank=True)
    secondry_phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    rent_sale_type = models.CharField(max_length=20, choices=R_S_TYPES, default="rent", null=True, blank=True)
    area = models.ForeignKey(Area, related_name="property_area", on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(Agent, related_name="individual_properties", on_delete=models.CASCADE, null=True, blank=True)
    company_agent = models.ForeignKey(CompanyAgent, related_name="company_properties", on_delete=models.CASCADE, null=True, blank=True)
    amenties = models.OneToOneField(PropertyAmenties, on_delete=models.CASCADE, null=True, blank=True)
    property_type = models.OneToOneField(PropertyTypes, on_delete=models.CASCADE, null=True, blank=True)
    property_location = models.OneToOneField(PropertyLocation, on_delete=models.CASCADE, null=True, blank=True)
    installment = models.OneToOneField(PropertyInstallment, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title}"


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