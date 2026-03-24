from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department

class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin display
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'department', 'role', 'is_staff']
    
    # Add custom fields to the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Team Info', {
            'fields': ('department', 'order_in_department', 'role', 'bio', 'photo', 'facebook', 'linkedin', 'portfolio')
        }),
    )
    
    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Team Info', {
            'fields': ('department', 'role')
        }),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
