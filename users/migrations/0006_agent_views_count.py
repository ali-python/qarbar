# Generated by Django 4.2.1 on 2023-09-18 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_agent_whatsapp_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]