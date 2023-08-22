from django.db import models
from django.utils import timezone
from core.models import DatedModel
from users.models import Agent
from company.models import CompanyAgent
from core.models import DatedModel
from property.models import (
    City, 
    Country, 
    PropertyTypes, 
    PropertyInstallment, 
    PropertyLocation, 
)

class PorjectAmenities(DatedModel):
    gymnasium = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    infinity_pool = models.BooleanField(default=False)
    childerns_play_area = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    leisure_lounge = models.BooleanField(default=False)
    retial_shop_outlet = models.BooleanField(default=False)
    near_by_hospital = models.BooleanField(default=False)
    near_by_school = models.BooleanField(default=False)
    near_by_shpping_mall = models.BooleanField(default=False)
    near_by_super_market = models.BooleanField(default=False)


class UnitType(models.Model):
    name = models.CharField(max_length=100)
    bed_count = models.PositiveIntegerField()
    size = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class ProjectBed(models.Model):
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    layout_type = models.CharField(max_length=50)
    bed_size = models.CharField(max_length=20)
    floor_plan_img = models.ImageField(upload_to='bed_floor_plans/', null=True, blank=True)

    def __str__(self):
        return f"{self.unit_type.name} - {self.layout_type} Bed"
    
class Document(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdf_files/')

class Projects(DatedModel):
    agent = models.ForeignKey(Agent, related_name="individua_agent", on_delete=models.CASCADE, null=True, blank=True)
    company_agent = models.ForeignKey(CompanyAgent, related_name="company_project", on_delete=models.CASCADE, null=True, blank=True)
    property_type = models.OneToOneField(PropertyTypes, on_delete=models.CASCADE, null=True, blank=True)
    property_location = models.OneToOneField(PropertyLocation, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    installment = models.OneToOneField(PropertyInstallment, on_delete=models.CASCADE, null=True, blank=True)
    amenities = models.OneToOneField(PorjectAmenities, on_delete=models.CASCADE, null=True, blank=True)
    available_units = models.OneToOneField(ProjectBed, on_delete=models.CASCADE, null=True, blank=True)
    brochure_document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    developer_name = models.CharField(max_length=250)
    title = models.CharField(max_length=200)
    delivery_date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

class Media(DatedModel):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('Video', 'Video'),
    )
    project = models.ForeignKey(Projects, related_name="property_media", on_delete=models.CASCADE, null=True, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default="image")
    image_url = models.CharField(max_length=250)
    
    def __str__(self):
        return self.media_type