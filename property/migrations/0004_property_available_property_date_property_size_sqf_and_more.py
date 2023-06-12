# Generated by Django 4.2.1 on 2023-06-08 15:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_city_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='property',
            name='size_sqf',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('villa', 'Villa'), ('house', 'House'), ('land', 'Land'), ('apartment', 'Apartment'), ('commercial', 'Commercial')], default='villa', max_length=20),
        ),
    ]
