# Generated by Django 4.2.1 on 2023-09-20 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='areas',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='languages',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='nationality',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
