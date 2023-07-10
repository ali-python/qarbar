from django.contrib import admin
from .models import Company, CustomUser, CompanyAgent

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address')
    search_fields = ('name', 'address')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_company')
    list_filter = ('is_company',)
    search_fields = ('username', 'email')

@admin.register(CompanyAgent)
class CompanyAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    list_filter = ('company',)
    search_fields = ('user__username', 'company__name')
