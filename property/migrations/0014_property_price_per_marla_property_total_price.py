# Generated by Django 4.2.1 on 2023-07-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_merge_20230718_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='price_per_marla',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='total_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
