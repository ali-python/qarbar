# Generated by Django 4.2.1 on 2023-09-20 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_agent_city_agent_cnic_agent_company_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
    ]
