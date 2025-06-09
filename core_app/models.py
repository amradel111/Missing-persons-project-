from django.db import models
from .choices import SOURCE_TYPE_CHOICES

class MissingPerson(models.Model):
    """
    Model to represent a missing person.
    """
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    last_seen_location = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class LiveVideoSource(models.Model):
    """
    Model to store sources of live video feeds (e.g., CCTV cameras).
    """
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='live_video_sources')
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES, default='url')
    url = models.URLField(max_length=500, blank=True, null=True, help_text="URL for the video stream (e.g., RTSP, HTTP)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} for {}".format(self.get_source_type_display(), self.missing_person.full_name)

class RecordedVideo(models.Model):
    """
    Model to store uploaded recorded video footage.
    """
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='recorded_videos')
    video_file = models.FileField(upload_to='recorded_videos/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )

    def __str__(self):
        return self.title


class SearchMatch(models.Model):
    """
    Represents a potential match found during a search.
    """
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='search_matches')
    live_video_source = models.ForeignKey(LiveVideoSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    recorded_video = models.ForeignKey(RecordedVideo, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    
    confidence_score = models.FloatField(help_text="Confidence score of the match (e.g., from face recognition)")
    snapshot_image = models.ImageField(upload_to='match_snapshots/', blank=True, null=True, help_text="Snapshot image of the match")
    timestamp = models.DateTimeField(auto_now_add=True)
    match_video_timestamp = models.CharField(max_length=20, blank=True, null=True, help_text="Timestamp in the recorded video where the match was found (e.g., 00:02:35).")

    def __str__(self):
        if self.recorded_video:
            source_info = "Video '{}' at {}".format(self.recorded_video.title, self.match_video_timestamp)
        else:
            source_info = "Live feed '{}'".format(self.live_video_source.id)
        return "Match for {} from {}".format(self.missing_person.full_name, source_info)

# ... existing code ...
