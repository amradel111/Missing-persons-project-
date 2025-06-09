from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
import json

from core_app.models import MissingPerson, MissingPersonImage, RecordedVideo, LiveVideoSource


@login_required
@require_http_methods(["GET"])
def get_missing_person(request, person_id):
    """API endpoint to get a missing person's details."""
    # Only return missing persons reported by the current user
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    
    # Format the date for the frontend
    last_seen_date = missing_person.last_seen_date.strftime('%Y-%m-%dT%H:%M')
    
    # Return the missing person data as JSON
    return JsonResponse({
        'id': missing_person.id,
        'full_name': missing_person.full_name,
        'age': missing_person.age,
        'gender': missing_person.gender or '',
        'last_seen_date': last_seen_date,
        'last_seen_location': missing_person.last_seen_location,
        'contact_phone': missing_person.contact_phone,
        'additional_info': missing_person.additional_info,
        'status': missing_person.status,
        'has_photo': bool(missing_person.photo),
        'photo_url': missing_person.photo.url if missing_person.photo else None,
    })

@login_required
def delete_missing_person(request, person_id):
    """Delete a missing person profile."""
    # Only delete profiles reported by the current user
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    
    # Get the name before deleting for the success message
    person_name = missing_person.full_name
    
    # Delete the profile
    missing_person.delete()
    
    messages.success(request, "Profile for '{}' has been deleted successfully.".format(person_name))
    return redirect('core_app:dashboard')

@login_required
@require_GET
def get_missing_person_images(request, person_id):
    """API endpoint to get all images for a missing person."""
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    images = MissingPersonImage.objects.filter(missing_person=missing_person)
    
    data = []
    for image in images:
        data.append({
            'id': image.id,
            'title': image.title,
            'url': image.image.url,
            'uploaded_at': image.uploaded_at
        })
    
    return JsonResponse(data, safe=False)

@login_required
@require_GET
def get_missing_person_videos(request, person_id):
    """API endpoint to get all videos for a missing person."""
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    videos = RecordedVideo.objects.filter(missing_person=missing_person)
    
    data = []
    for video in videos:
        data.append({
            'id': video.id,
            'title': video.title,
            'url': video.video.url,
            'thumbnail': video.thumbnail.url if video.thumbnail else None,
            'uploaded_at': video.uploaded_at
        })
    
    return JsonResponse(data, safe=False)

@login_required
@require_GET
def get_missing_person_live_sources(request, person_id):
    """API endpoint to get all live sources for a missing person."""
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    sources = LiveVideoSource.objects.filter(missing_person=missing_person)
    
    data = []
    for source in sources:
        data.append({
            'id': source.id,
            'title': source.title,
            'source_type': source.source_type,
            'url': source.url,
            'is_active': source.is_active,
            'created_at': source.created_at
        })
    
    return JsonResponse(data, safe=False) 