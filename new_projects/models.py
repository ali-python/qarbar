from django.db import models
from django.utils import timezone
from core.models import DatedModel
from users.models import Agent
from company.models import CompanyAgent
from property.models import (
    PropertyAmenties,
    City, 
    Country, 
    PropertyTypes, 
    PropertyInstallment, 
    PropertyLocation, 
    Media
)

