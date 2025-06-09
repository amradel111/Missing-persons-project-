from django.db import models
from .missing_person import MissingPerson # Assuming MissingPerson is in missing_person.py
from .media import LiveVideoSource # Assuming LiveVideoSource is in media.py

class SearchMatch(models.Model):
    """
    Model to store records of successful face recognition matches during a search.
    """
    missing_person = models.ForeignKey(
        MissingPerson, 
        on_delete=models.CASCADE, 
        related_name='search_matches'
    )
    live_video_source = models.ForeignKey(
        LiveVideoSource, 
        on_delete=models.SET_NULL, # Keep match record even if source is deleted
        related_name='matches_found_via_source',
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    confidence_score = models.FloatField(null=True, blank=True)
    snapshot_image = models.ImageField(
        upload_to='search_snapshots/%Y/%m/%d/', 
        null=True, 
        blank=True, 
        help_text="A snapshot frame where the match occurred."
    )
    # Add other relevant fields if needed, e.g., bounding_box_data (JSONField)

    def __str__(self):
        return "Match for {} at {}".format(self.missing_person.full_name, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = "Search Match"
        verbose_name_plural = "Search Matches"
        ordering = ['-timestamp'] 