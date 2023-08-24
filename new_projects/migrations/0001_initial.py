# Generated by Django 4.2.1 on 2023-08-08 14:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('property', '0019_alter_propertytypes_commercial_types_and_more'),
        ('users', '0002_agent_created_at_agent_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pdf_file', models.FileField(upload_to='pdf_files/')),
            ],
        ),
        migrations.CreateModel(
            name='PorjectAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('gymnasium', models.BooleanField(default=False)),
                ('swimming_pool', models.BooleanField(default=False)),
                ('infinity_pool', models.BooleanField(default=False)),
                ('childerns_play_area', models.BooleanField(default=False)),
                ('restaurant', models.BooleanField(default=False)),
                ('leisure_lounge', models.BooleanField(default=False)),
                ('retial_shop_outlet', models.BooleanField(default=False)),
                ('near_by_hospital', models.BooleanField(default=False)),
                ('near_by_school', models.BooleanField(default=False)),
                ('near_by_shpping_mall', models.BooleanField(default=False)),
                ('near_by_super_market', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectBed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout_type', models.CharField(max_length=50)),
                ('bed_size', models.CharField(max_length=20)),
                ('floor_plan_img', models.ImageField(upload_to='bed_floor_plans/')),
            ],
        ),
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bed_count', models.PositiveIntegerField()),
                ('size', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('developer_name', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=200)),
                ('delivery_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('total_price', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individua_agent', to='users.agent')),
                ('amenities', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='new_projects.porjectamenities')),
                ('available_units', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='new_projects.projectbed')),
                ('brochure_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='new_projects.document')),
                ('city', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.city')),
                ('company_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_project', to='company.companyagent')),
                ('country', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.country')),
                ('installment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.propertyinstallment')),
                ('property_location', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.propertylocation')),
                ('property_type', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.propertytypes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='projectbed',
            name='unit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_projects.unittype'),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('Video', 'Video')], default='image', max_length=20)),
                ('image_url', models.CharField(max_length=250)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_media', to='new_projects.projects')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]