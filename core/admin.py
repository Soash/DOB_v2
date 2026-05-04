from django.contrib import admin
from .models import BSDSItem, BlogCategory, BlogPost, ResearchPaper, Feedback, Carrier

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

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at')
    list_filter = ('published', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'publication_date')
    search_fields = ('title', 'authors', 'journal')
    list_filter = ('publication_date', 'journal')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation', 'star_count')
    search_fields = ('name', 'occupation', 'comment')
    list_filter = ('star_count',)

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('title', 'employment_type', 'location', 'posted_date', 'deadline', 'is_active')
    list_filter = ('is_active', 'employment_type', 'location')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}