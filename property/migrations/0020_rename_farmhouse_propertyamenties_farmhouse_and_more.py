# Generated by Django 4.2.1 on 2023-08-11 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_alter_propertyamenties_bathrooms_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='propertyamenties',
            old_name='Farmhouse',
            new_name='farmhouse',
        ),
        migrations.RenameField(
            model_name='propertytypes',
            old_name='size_sqf',
            new_name='size',
        ),
    ]