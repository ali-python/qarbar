from django.contrib import admin
from .models import City, Property, Country, Media, Area
from django.utils.html import format_html


class MediaTabularAdmin(admin.TabularInline):
    model = Media

class CountryMedia(admin.ModelAdmin):
    list_display = ('property_type', 'image_url')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code', 'date')

class CityAdmin(admin.ModelAdmin):
    list_display = ('country','city_name', 'city_code', 'date')

class AreaAdmin(admin.ModelAdmin):
    list_display = ('city','area')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'R_B_type', 'size_sqf', 'area', 'bedrooms', 'bathrooms', 'kitchen', 'floors', 'maid_room',
                    'car_porch', 'agent', 'available', 'date')
    list_filter = ('property_type',)
    inlines = [MediaTabularAdmin,]

class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'property','media_type')
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
