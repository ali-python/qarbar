# Generated by Django 4.2.1 on 2023-08-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0021_merge_20230826_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyamenties',
            name='balcony',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='bathrooms',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='bedrooms',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='built_in_wardrobes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='built_in_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='community_lawn_garden',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='covered_parking',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='distance_from_airport',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='drawing_room',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='electricity_backup',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='farmhouse',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='floors',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='furnished_unfurnished',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='gym',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='internet',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='kids_play_area',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='kitchen',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='kitchen_appliances',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='laundry_room',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='lobby_in_building',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='lounge_sitting_area',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='lower_portion',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='maid_room',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='medical_center',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='mosque',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='near_by_hospital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='near_by_school',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='near_by_shopping_mall',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='other_description',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='other_nearby_palces',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='parking_space',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='security',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='store_room',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='study_room',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyamenties',
            name='swimming_pool',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='propertyinstallment',
            name='advance_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='propertyinstallment',
            name='monthly_inst',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='propertyinstallment',
            name='no_of_inst',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='propertyinstallment',
            name='ready_for_possession',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
