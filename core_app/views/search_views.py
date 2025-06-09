from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
import base64
import uuid
import json
import requests
from django.conf import settings
from django.urls import reverse

from core_app.models import MissingPerson, LiveVideoSource, SearchMatch

@login_required
def live_search_redirect(request):
    """
    View to handle the redirect from the search button.
    Gets the person_id from the query parameters and finds an appropriate webcam source.
    """
    person_id = request.GET.get('person_id')
    source_id = request.GET.get('source_id')  # Get the specific source ID if provided
    device_id = request.GET.get('device_id')  # Get the webcam device ID if provided

    if not person_id:
        return HttpResponseBadRequest("Missing person ID")
    
    try:
        # Get the person and verify ownership
        person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        # If a specific source_id is provided, use it
        if source_id:
            try:
                webcam_source = LiveVideoSource.objects.get(id=source_id, missing_person=person, source_type='webcam')
                # Include device_id parameter if provided
                redirect_url = reverse('core_app:live_search_page', kwargs={'person_id': person.id, 'source_id': webcam_source.id})
                if device_id:
                    redirect_url += '?device_id={}'.format(device_id)
                return redirect(redirect_url)
            except LiveVideoSource.DoesNotExist:
                # If the provided source_id is invalid or doesn't belong to the user,
                # fall through to the default behavior.
                pass

        # Default behavior: Find the first available webcam source or create a new one
        webcam_source = LiveVideoSource.objects.filter(
            missing_person=person,
            source_type='webcam'
        ).first()
        
        if webcam_source:
            # Redirect to the live search page with this source
            redirect_url = reverse('core_app:live_search_page', kwargs={'person_id': person.id, 'source_id': webcam_source.id})
            if device_id:
                redirect_url += '?device_id={}'.format(device_id)
            return redirect(redirect_url)
        else:
            # Create a new webcam source
            webcam_source = LiveVideoSource.objects.create(
                missing_person=person,
                source_type='webcam',
                url="webcam://auto-created"
            )
            redirect_url = reverse('core_app:live_search_page', kwargs={'person_id': person.id, 'source_id': webcam_source.id})
            if device_id:
                redirect_url += '?device_id={}'.format(device_id)
            return redirect(redirect_url)
            
    except Exception as e:
        return HttpResponseBadRequest("Error: {}".format(str(e)))

@login_required
def live_search_page(request, person_id, source_id):
    """
    Page to display live webcam feed and run face detection for a specific missing person.
    """
    missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
    # Ensure the source_id is valid and related to this person, or handle general webcam case
    # For now, we assume source_id might refer to a configured LiveVideoSource or be a generic indicator
    # For a generic webcam, source_id might not map directly to a LiveVideoSource record initially
    live_source = None
    if source_id != 0: # Assuming 0 could mean generic local webcam not tied to a specific DB record yet
        try:
            live_source = get_object_or_404(LiveVideoSource, id=source_id, missing_person=missing_person)
        except LiveVideoSource.DoesNotExist:
            # Potentially handle case where source_id is invalid for the person
            # For now, we'll allow it to proceed if source_id is non-zero but not found, 
            # implying a new dynamic source not yet saved, or just default to webcam.
            pass 

    # Get the missing person's photo URL - use primary photo if available
    person_photo_url = None
    if missing_person.photo:
        person_photo_url = request.build_absolute_uri(missing_person.photo.url)
    else:
        # If no primary photo, try to get the first uploaded image
        first_image = missing_person.additional_images.first()
        if first_image:
            person_photo_url = request.build_absolute_uri(first_image.image.url)

    # The URL for the face recognition service (FastAPI)
    # Ensure this is configurable, e.g., via Django settings
    face_recognition_service_url = "http://localhost:8003/detect/" 

    context = {
        'missing_person': missing_person,
        'live_source': live_source, # Can be None if it's a generic webcam scenario
        'person_photo_url': person_photo_url,
        'face_recognition_service_url': face_recognition_service_url,
        'source_id_for_logging': source_id if live_source else None # Pass the original source_id if live_source resolved
    }
    return render(request, 'core_app/live_search.html', context)

@login_required
@require_POST
def log_match_view(request):
    """
    API endpoint to log a successful face recognition match.
    """
    try:
        data = json.loads(request.body)
        person_id = data.get('person_id')
        source_id = data.get('source_id') # This might be the ID of a LiveVideoSource or null/0 for generic webcam
        confidence_score = data.get('confidence_score')
        frame_data_base64 = data.get('frame_data') # Base64 snapshot

        if not person_id:
            return HttpResponseBadRequest("Missing person_id")

        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        live_source_instance = None
        if source_id:
            try:
                live_source_instance = LiveVideoSource.objects.get(id=source_id, missing_person=missing_person)
            except LiveVideoSource.DoesNotExist:
                # Log a warning or handle as appropriate if source_id is provided but not found
                print("Warning: LiveVideoSource with id {} not found for person {}.".format(source_id, person_id))
                pass # Proceed to save match without specific source linkage if it's not critical

        match = SearchMatch.objects.create(
            missing_person=missing_person,
            live_video_source=live_source_instance,
            confidence_score=confidence_score
        )

        if frame_data_base64:
            try:
                format, imgstr = frame_data_base64.split(';base64,') 
                ext = format.split('/')[-1] 
                image_data = base64.b64decode(imgstr)
                file_name = 'snapshot_{}.{}'.format(uuid.uuid4().hex, ext)
                match.snapshot_image.save(file_name, ContentFile(image_data), save=True)
            except Exception as e:
                print("Error saving snapshot image for match {}: {}".format(match.id, e))
                # Log this error but don't fail the whole match logging

        return JsonResponse({'success': True, 'match_id': match.id, 'message': 'Match logged successfully.'}, status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data.")
    except Exception as e:
        print("Error in log_match_view: {}".format(e))
        return JsonResponse({'success': False, 'error': str(e)}, status=500) 