from django.contrib import admin
from .models import UserProfile, Device, BirdDetection, ActivityLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'contact_number', 'province', 'created_at']
    search_fields = ['full_name', 'contact_number']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active']
    search_fields = ['name', 'location']


@admin.register(BirdDetection)
class BirdDetectionAdmin(admin.ModelAdmin):
    list_display = ['device', 'bird_count', 'bird_species', 'confidence_score', 'detected_at']
    list_filter = ['bird_species', 'detected_at']
    date_hierarchy = 'detected_at'


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'event_type', 'description', 'created_at']
    list_filter = ['event_type', 'created_at']
    date_hierarchy = 'created_at'
