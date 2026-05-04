from django.contrib import admin
from .models import BSDSEvent


@admin.register(BSDSEvent)
class BSDSEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_text')
    search_fields = ('title', 'date_text')
