# Generated by Django 4.2.1 on 2023-08-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_alter_propertyamenties_distance_from_airport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyamenties',
            name='built_in_year',
            field=models.IntegerField(null=True),
        ),
    ]
