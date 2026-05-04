from django.contrib import admin
from .models import BSDSEvent, CampusSeminar, SeminarProgramConfig


@admin.register(BSDSEvent)
class BSDSEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_text')
    search_fields = ('title', 'date_text')


@admin.register(CampusSeminar)
class CampusSeminarAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'university_name', 'event_description', 'order')
    list_editable = ('order',)
    search_fields = ('abbreviation', 'university_name')


@admin.register(SeminarProgramConfig)
class SeminarProgramConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Program Card Links', {
            'fields': ('bio_seminar_url', 'clinical_seminar_url', 'training_program_url'),
            'description': 'Links for the three "Request This Program" buttons on the seminar cards.',
        }),
        ('Quiz Button', {
            'fields': ('quiz_url',),
            'description': 'Link for the "Take the Seminar Quiz" button.',
        }),
    )

    def has_add_permission(self, request):
        # Enforce singleton — only allow adding if none exists
        return not SeminarProgramConfig.objects.exists()
