# Generated by Django 4.2.1 on 2023-09-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_agent_areas_alter_agent_bio_alter_agent_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
