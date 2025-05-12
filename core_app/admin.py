from django.contrib import admin
from .models import MissingPerson, MissingPersonImage, RecordedVideo, LiveVideoSource, SearchMatch

@admin.register(MissingPerson)
class MissingPersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'gender', 'status', 'last_seen_date', 'reported_by', 'created_at')
    list_filter = ('status', 'gender', 'created_at', 'last_seen_date')
    search_fields = ('full_name', 'last_seen_location', 'additional_info')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'age', 'gender', 'photo')
        }),
        ('Last Seen Details', {
            'fields': ('last_seen_date', 'last_seen_location')
        }),
        ('Contact & Additional Info', {
            'fields': ('contact_phone', 'additional_info')
        }),
        ('Record Management', {
            'fields': ('reported_by', 'status', 'created_at', 'updated_at')
        }),
    )

@admin.register(MissingPersonImage)
class MissingPersonImageAdmin(admin.ModelAdmin):
    list_display = ('missing_person', 'title', 'image', 'uploaded_at')
    list_filter = ('missing_person__full_name', 'uploaded_at')
    search_fields = ('title', 'missing_person__full_name')

@admin.register(RecordedVideo)
class RecordedVideoAdmin(admin.ModelAdmin):
    list_display = ('missing_person', 'title', 'video', 'duration', 'uploaded_at')
    list_filter = ('missing_person__full_name', 'uploaded_at')
    search_fields = ('title', 'missing_person__full_name')

@admin.register(LiveVideoSource)
class LiveVideoSourceAdmin(admin.ModelAdmin):
    list_display = ('missing_person', 'title', 'source_type', 'url', 'is_active', 'created_at')
    list_filter = ('source_type', 'is_active', 'missing_person__full_name', 'created_at')
    search_fields = ('title', 'url', 'missing_person__full_name')

@admin.register(SearchMatch)
class SearchMatchAdmin(admin.ModelAdmin):
    list_display = ('missing_person', 'live_video_source', 'timestamp', 'confidence_score')
    list_filter = ('missing_person__full_name', 'timestamp', 'live_video_source__title')
    search_fields = ('missing_person__full_name',)
    readonly_fields = ('timestamp',) 