from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from core.models import DatedModel
from django.utils import timezone

class UserProfile(DatedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Agent(DatedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True ,related_name='agent')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_ntn = models.CharField(max_length=100, null=True, blank=True)
    cnic = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_num = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    bio = models.TextField()
    nationality = models.CharField(max_length=50)
    languages = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    areas= models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    experience_since = models.DateField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Signal Functions
def create_profile(sender, instance, created, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not UserProfile.objects.filter(user=instance):
        UserProfile.objects.get_or_create(
            user=instance
        )


# Signals    
post_save.connect(create_profile, sender=User)
