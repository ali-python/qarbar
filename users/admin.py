from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Agent


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'dob', 'city', 'country')
    search_fields = ('user__username', 'user__email')


class AgentAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'email', 'phone_number', 'nationality', 'languages', 'areas', 'experience_since')
    list_filter = ('nationality', 'languages', 'areas')
    search_fields = ('name', 'email', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Agent, AgentAdmin)
