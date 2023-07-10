from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)

        # Add the related_name and related_query_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        related_query_name='user_group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        related_query_name='user_permission',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    
class CompanyAgent(models.Model):
    user = models.OneToOneField(CustomUser,related_name="company_users", related_query_name="company_users", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="agents_company", related_query_name="agents_company", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username