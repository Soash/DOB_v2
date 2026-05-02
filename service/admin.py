from django.contrib import admin
from .models import ServiceCategory, Service, ServiceImage, ServiceFAQ

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    search_fields = ('name',)

# --- Inlines for related models ---
class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1  # Provides 1 blank row by default to add new images

class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1  # Provides 1 blank row by default to add new FAQs

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Displays the thumbnail info, active status, and allows quick order editing
    list_display = ('title', 'category', 'is_active', 'is_top', 'order')
    list_filter = ('category', 'is_active', 'is_top')
    search_fields = ('title', 'description', 'introduction_description', 'features_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'order', 'is_top')
    
    # Groups the fields nicely in the admin form view
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'description')
        }),
        ('Detailed Content', {
            'fields': ('introduction_description', 'features_description', 'demo_description'),
            'classes': ('collapse',),  # Makes this section collapsible to keep the UI tidy
            'description': 'Additional detailed content blocks for the single service page.'
        }),
        ('Media & Links', {
            'fields': ('thumbnail', 'learn_more_url')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'is_top', 'order')
        }),
    )
    
    # Connects the Image and FAQ models directly to the Service admin page
    inlines = [ServiceImageInline, ServiceFAQInline]


from .models import ClinicalService, ClinicalServiceImage, ClinicalServiceFAQ

class ClinicalServiceImageInline(admin.TabularInline):
    model = ClinicalServiceImage
    extra = 1

class ClinicalServiceFAQInline(admin.TabularInline):
    model = ClinicalServiceFAQ
    extra = 1

@admin.register(ClinicalService)
class ClinicalServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Icon & Styling', {
            'fields': ('icon_svg', 'icon_color'),
            'description': 'Provide raw SVG code (using currentColor) and a Tailwind color (e.g. blue, purple, cyan).'
        }),
        ('Detailed Content', {
            'fields': ('introduction_description', 'features_description', 'demo_description'),
            'classes': ('collapse',),
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
    )
    
    inlines = [ClinicalServiceImageInline, ClinicalServiceFAQInline]