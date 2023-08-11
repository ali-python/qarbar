from django.contrib import admin
from django.utils.html import format_html
from .models import (
    City, Property, 
    Country, 
    Media,
    Area,
    PropertyLocation,
    PropertyAmenties, 
    PropertyTypes, 
    PropertyInstallment
    )

class MediaTabularAdmin(admin.TabularInline):
    model = Media

class CountryMedia(admin.ModelAdmin):
    list_display = ('property_type', 'image_url')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')

class CityAdmin(admin.ModelAdmin):
    list_display = ('country', 'city_name', 'city_code')

class AreaAdmin(admin.ModelAdmin):
    list_display = ('city', 'area')

class PropertyAmentiesAdmin(admin.ModelAdmin):
    list_display = [
        'other_nearby_palces', 'bedrooms', 'distance_from_airport', 'built_in_year', 'bathrooms',
        'kitchen', 'floors', 'maid_room', 'built_in_wardrobes', 'kitchen_appliances', 'balcony',
        'lower_portion', 'farmhouse', 'electricity_backup', 'furnished_unfurnished', 'covered_parking',
        'lobby_in_building', 'security', 'parking_space', 'drawing_room', 'study_room', 'laundry_room',
        'store_room', 'gym', 'lounge_sitting_area', 'internet', 'swimming_pool', 'mosque', 'kids_play_area',
        'medical_center', 'community_lawn_garden', 'near_by_school', 'near_by_hospital', 'near_by_shopping_mall',
        'other_description'
    ]

class PropertyTypesAdmin(admin.ModelAdmin):
    list_display = [
        'plot_types', 'home_types', 'commercial_types', 'unit_types', 'size', 'other_description'
    ]

class PropertyInstallmentAdmin(admin.ModelAdmin):
    list_display = ['advance_amount', 'no_of_inst', 'monthly_inst', 'ready_for_possession']

class PropertyAmentiesInline(admin.TabularInline):
    model = PropertyAmenties
    can_delete = False

class PropertyTypesInline(admin.TabularInline):
    model = PropertyTypes
    can_delete = False

class PropertyInstallmentInline(admin.TabularInline):
    model = PropertyInstallment
    can_delete = False

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'rent_sale_type', 'area', 'agent', 'company_agent', 'available', 'total_price', 'date']
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, (PropertyAmentiesInline, PropertyTypesInline, PropertyInstallmentInline, MediaTabularAdmin)):
                if obj and getattr(obj, inline.model.__name__.lower(), None):
                    # Remove the ForeignKey instance for OneToOne fields.
                    setattr(obj, inline.model.__name__.lower(), None)
            yield inline.get_formset(request, obj), inline

class PropertyLocationAdmin(admin.ModelAdmin):
    list_display = ('property', 'latitude', 'longitude')


class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'property', 'media_type')
    raw_id_fields = ('property',)
    model = Media
    
    def property_image(self, obj):
        return format_html(
            f'<a href="{obj.image_url}" target="_blank"><img src="{obj.image_url}" width="100" height="100" /><a>'
            )
    
admin.site.register(Media, MediaAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyLocation, PropertyLocationAdmin)
admin.site.register(PropertyAmenties, PropertyAmentiesAdmin)
admin.site.register(PropertyTypes, PropertyTypesAdmin)
admin.site.register(PropertyInstallment, PropertyInstallmentAdmin)

