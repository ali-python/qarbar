# Generated by Django 4.2.1 on 2023-10-05 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0024_property_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='admin_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_property', to=settings.AUTH_USER_MODEL),
        ),
    ]
