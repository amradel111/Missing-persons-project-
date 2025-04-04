from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from core_app.models import MissingPerson


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
    
    messages.success(request, f"Profile for '{person_name}' has been deleted successfully.")
    return redirect('core_app:dashboard') 