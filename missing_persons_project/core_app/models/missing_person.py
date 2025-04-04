from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MissingPerson(models.Model):
    """
    Model to store information about missing persons.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('missing', 'Missing'),
        ('found', 'Found'),
        ('resolved', 'Case Resolved'),
    ]

    # Basic information
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Last seen information
    last_seen_date = models.DateTimeField()
    last_seen_location = models.CharField(max_length=255)
    
    # Contact information
    contact_phone = models.CharField(max_length=20)
    
    # Additional details
    additional_info = models.TextField(blank=True)
    photo = models.ImageField(upload_to='missing_persons/', blank=True, null=True)
    
    # Record metadata
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_persons')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='missing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.age})"
    
    class Meta:
        verbose_name = "Missing Person"
        verbose_name_plural = "Missing Persons"
        ordering = ['-created_at']
        
    def time_since_missing(self):
        """Return the time elapsed since the person was reported missing."""
        now = timezone.now()
        elapsed = now - self.last_seen_date
        
        if elapsed.days > 0:
            return f"{elapsed.days} day{'s' if elapsed.days != 1 else ''}"
        hours = elapsed.seconds // 3600
        if hours > 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        minutes = (elapsed.seconds % 3600) // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}" 