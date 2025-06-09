from django.db import models
from django.utils import timezone
from core_app.models import MissingPerson

class MissingPersonImage(models.Model):
    """
    Model to store additional images of a missing person.
    """
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='missing_persons_images/')
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {}".format(self.title, self.missing_person.full_name)
    
    def save(self, *args, **kwargs):
        # Auto-generate title if not provided
        if not self.title:
            # Count existing images and add 1
            count = MissingPersonImage.objects.filter(missing_person=self.missing_person).count() + 1
            self.title = "Image {}".format(count)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-uploaded_at']

class RecordedVideo(models.Model):
    """
    Model to store recorded videos to search for a missing person.
    """
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='recorded_videos')
    video = models.FileField(upload_to='missing_persons_videos/')
    title = models.CharField(max_length=255, blank=True)
    duration = models.DurationField(null=True, blank=True)  # Duration in seconds
    thumbnail = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {}".format(self.title, self.missing_person.full_name)
    
    def save(self, *args, **kwargs):
        # Auto-generate title if not provided
        if not self.title:
            # Count existing videos and add 1
            count = RecordedVideo.objects.filter(missing_person=self.missing_person).count() + 1
            self.title = "Video {}".format(count)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-uploaded_at']

class LiveVideoSource(models.Model):
    """
    Model to store information about live video sources to search for a missing person.
    """
    SOURCE_TYPES = [
        ('url', 'URL Stream'),
        ('webcam', 'Webcam'),
    ]
    
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='live_video_sources')
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    url = models.URLField(max_length=255, blank=True, null=True) 
    title = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {}".format(self.title, self.missing_person.full_name)
    
    def save(self, *args, **kwargs):
        # Auto-generate title if not provided
        if not self.title:
            # Count existing live sources and add 1
            count = LiveVideoSource.objects.filter(missing_person=self.missing_person).count() + 1
            self.title = "Live Source {}".format(count)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at'] 