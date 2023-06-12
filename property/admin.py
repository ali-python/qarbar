from django.contrib import admin
from .models import City, Property, Country

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code', 'date')

class CityAdmin(admin.ModelAdmin):
    list_display = ('country','city_name', 'city_code', 'date')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_type','size_sqf', 'city', 'bedrooms', 'bathrooms', 'kitchen', 'floors', 'maid_room',
                    'car_porch', 'agent', 'buy_rent','available','date')
    list_filter = ('property_type', 'city', 'buy_rent')

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Property, PropertyAdmin)
