from django.http import JsonResponse
from .upload_views import (
    upload_media_page, upload_person_image, upload_recorded_video,
    add_live_url, add_webcam_source, delete_media
)

def placeholder(request):
    """Simple placeholder view for testing."""
    return JsonResponse({'status': 'ok', 'message': 'API is working'})

__all__ = [
    'placeholder',
    'upload_media_page',
    'upload_person_image',
    'upload_recorded_video',
    'add_live_url',
    'add_webcam_source',
    'delete_media'
]
