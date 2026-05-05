from django.contrib import admin
from .models import BSDSEvent, CampusSeminar, SeminarProgramConfig, CampusCoordinator, Collaboration, Competition, ResearchTalk


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


@admin.register(CampusCoordinator)
class CampusCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'role_label', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'year', 'role_label')


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('name', 'collab_type', 'icon', 'order')
    list_editable = ('order',)
    list_filter = ('collab_type',)
    search_fields = ('name',)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'placement', 'year', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'placement', 'year')
    search_fields = ('title',)


@admin.register(ResearchTalk)
class ResearchTalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
