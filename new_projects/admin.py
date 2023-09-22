from django.contrib import admin
from .models import PorjectAmenities, UnitType, ProjectBed, Document, Projects, Media

class PorjectAmenitiesAdmin(admin.ModelAdmin):
    list_display = (
        'id','gymnasium', 'swimming_pool', 'infinity_pool', 'childerns_play_area',
        'restaurant', 'leisure_lounge', 'retial_shop_outlet',
        'near_by_hospital', 'near_by_school', 'near_by_shpping_mall',
        'near_by_super_market'
    )

class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'bed_count', 'size')

class ProjectBedAdmin(admin.ModelAdmin):
    list_display = ('unit_type', 'layout_type', 'bed_size')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'pdf_file')

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer_name', 'delivery_date', 'status')
    list_filter = ('status', 'developer_name', 'delivery_date')
    search_fields = ('title', 'developer_name', 'property_location__name')
    date_hierarchy = 'delivery_date'

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Media)
admin.site.register(Document, DocumentAdmin)
admin.site.register(ProjectBed, ProjectBedAdmin)
admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(PorjectAmenities, PorjectAmenitiesAdmin)
