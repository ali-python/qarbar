# Generated by Django 4.2.1 on 2023-07-31 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0017_remove_property_size_sqf_propertytypes_size_sqf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='mobile',
            new_name='secondry_phone',
        ),
        migrations.RemoveField(
            model_name='property',
            name='R_B_type',
        ),
        migrations.RemoveField(
            model_name='propertylocation',
            name='property',
        ),
        migrations.AddField(
            model_name='property',
            name='property_location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.propertylocation'),
        ),
        migrations.AddField(
            model_name='property',
            name='rent_sale_type',
            field=models.CharField(blank=True, choices=[('rent', 'Rent'), ('sale', 'Sale')], default='rent', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='phone',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='commercial_types',
            field=models.CharField(blank=True, choices=[('office', 'Office'), ('shop', 'Shop'), ('warehouse', 'WareHouse'), ('factory', 'Factory'), ('building', 'Building'), ('other', 'other')], default='office', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='home_types',
            field=models.CharField(blank=True, choices=[('house', 'House'), ('flat', 'Flat'), ('upper_portion', 'Uper Portion'), ('lower_portion', 'Lower Portion'), ('farm_house', 'Farm House'), ('room', 'Room'), ('pent_house', 'Pent House')], default='house', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='other_description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='plot_types',
            field=models.CharField(blank=True, choices=[('residetial_plot', 'Residential Plot'), ('commercial_plot', 'Commercial Plot'), ('agricultural_land', 'Agricultural Land'), ('Industrial_land', 'Industrial_Land'), ('plot_file', 'Plot File'), ('plot_form', 'Plot Form')], default='residetial_plot', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='size_sqf',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='propertytypes',
            name='unit_types',
            field=models.CharField(blank=True, choices=[('marla', 'Marla'), ('sqft', 'Sq.Ft.'), ('sqm', 'Sq.M.'), ('sqyd', 'Sq.Yd.'), ('kanal', 'Kanal')], default='marla', max_length=100, null=True),
        ),
    ]
