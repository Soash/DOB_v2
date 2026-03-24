from django.contrib import admin
from .models import BSDSItem

@admin.register(BSDSItem)
class BSDSItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Media & Links', {
            'fields': ('thumbnail', 'details_url')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
    )