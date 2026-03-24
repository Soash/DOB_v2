from django.contrib import admin
from .models import ServiceCategory, Service

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Displays the thumbnail info, active status, and allows quick order editing
    list_display = ('title', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'order')
    
    # Groups the fields nicely in the admin form view
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'description')
        }),
        ('Media & Links', {
            'fields': ('thumbnail', 'learn_more_url')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
    )