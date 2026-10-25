from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, CareerProgression, Education

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ['degree', 'department', 'university', 'country', 'order']

class CareerProgressionInline(admin.TabularInline):
    model = CareerProgression
    extra = 1
    fields = ['title', 'organization', 'start_date', 'end_date', 'period', 'is_current', 'order', 'description']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'department', 'role', 'is_staff']
    list_filter = ['department', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'role']
    inlines = [EducationInline, CareerProgressionInline]
    
    fieldsets = UserAdmin.fieldsets + (
        ('Team & Role Info', {
            'fields': (
                'department',
                'order_in_department',
                'role',
                'bio',
                'photo',
            )
        }),
        ('Education & Qualifications', {
            'description': 'Add degrees like BSc, MSc, or PhD below, or use the Education table at the bottom to add multiple degrees.',
            'fields': (
                'degree',
                'university_department',
                'university',
                'country',
                'education',
                'skills',
            )
        }),
        ('Career Progression Details', {
            'fields': (
                'career_progression_details',
            )
        }),
        ('Social & Professional Profiles', {
            'fields': (
                'linkedin',
                'portfolio',
                'github',
                'researchgate',
                'google_scholar',
                'twitter',
                'facebook',
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Team Info', {
            'fields': ('department', 'role')
        }),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']

class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree', 'department', 'university', 'country', 'order']
    list_filter = ['user', 'country']
    search_fields = ['degree', 'department', 'university', 'country', 'user__username', 'user__first_name', 'user__last_name']
    list_editable = ['order']

class CareerProgressionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'organization', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['user', 'is_current']
    search_fields = ['title', 'organization', 'user__username', 'user__first_name', 'user__last_name']
    list_editable = ['order', 'is_current']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(CareerProgression, CareerProgressionAdmin)
