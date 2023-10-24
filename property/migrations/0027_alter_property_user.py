# Generated by Django 4.2.1 on 2023-10-23 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0026_remove_property_area_propertylocation_city_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_property', to=settings.AUTH_USER_MODEL),
        ),
    ]
