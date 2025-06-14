from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import models
import json
import os
import uuid

from core_app.models import MissingPerson, MissingPersonImage, RecordedVideo, LiveVideoSource
from core_app.forms import MissingPersonImageForm, RecordedVideoForm, LiveVideoUrlForm, LiveVideoWebcamForm

# Add these imports for chunked uploads
from django.conf import settings
import shutil

@login_required
def upload_media_page(request):
    """
    View for the upload media page where users can upload images, videos, and link live footage
    for missing persons.
    """
    # Get all missing persons reported by the current user
    # and prefetch their webcam live sources
    missing_persons_qs = MissingPerson.objects.filter(
        reported_by=request.user
    ).prefetch_related(
        models.Prefetch(
            'live_video_sources',
            queryset=LiveVideoSource.objects.filter(source_type='webcam'),
            to_attr='webcam_sources'
        )
    )

    missing_persons_list = []
    for person in missing_persons_qs:
        # The webcam_sources attribute is now directly on the person object due to to_attr
        # If you expect only one active webcam source, you might want to get person.webcam_sources[0] if person.webcam_sources else None
        missing_persons_list.append({
            'person': person,
            'webcam_sources': person.webcam_sources # This will be a list of webcam LiveVideoSource objects
        })
    
    # Initialize all forms
    image_form = MissingPersonImageForm()
    video_form = RecordedVideoForm()
    url_form = LiveVideoUrlForm()
    webcam_form = LiveVideoWebcamForm()
    
    context = {
        'missing_persons_data': missing_persons_list, # Changed from missing_persons
        'image_form': image_form,
        'video_form': video_form,
        'url_form': url_form,
        'webcam_form': webcam_form,
    }
    
    return render(request, 'core_app/upload_media.html', context)

@login_required
@require_POST
def upload_person_image(request, person_id):
    """
    API endpoint to handle uploading a missing person's image.
    """
    try:
        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        if 'image' not in request.FILES:
            return JsonResponse({'success': False, 'errors': {'image': ['No image file provided.']}}, status=400)
        
        # Get the uploaded image file
        image_file = request.FILES['image']
        
        # Create the image record
        image = MissingPersonImage(
            missing_person=missing_person,
            image=image_file
        )
        image.save()
        
        return JsonResponse({
            'success': True,
            'image_id': image.id,
            'title': image.title,
            'url': image.image.url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@login_required
@require_POST
def upload_recorded_video(request, person_id):
    """
    API endpoint to handle uploading a recorded video for search.
    """
    try:
        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        if 'video' not in request.FILES:
            return JsonResponse({'success': False, 'errors': {'video': ['No video file provided.']}}, status=400)
        
        # Get the uploaded video file
        video_file = request.FILES['video']
        
        # Create the video record
        video = RecordedVideo(
            missing_person=missing_person,
            video=video_file
        )
        video.save()
        
        # Ensure we return both url and video_url for backward compatibility
        video_url = video.video.url
        
        return JsonResponse({
            'success': True,
            'video_id': video.id,
            'title': video.title,
            'url': video_url,
            'video_url': video_url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

# Add new endpoint for chunked uploads
@login_required
@require_POST
def upload_chunk(request, person_id):
    """
    API endpoint to handle uploading large files in chunks.
    """
    try:
        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        # Get chunk metadata from request
        chunk_number = int(request.POST.get('chunk_number', 0))
        total_chunks = int(request.POST.get('total_chunks', 0))
        file_type = request.POST.get('file_type', '')  # 'image' or 'video'
        file_id = request.POST.get('file_id', '')
        
        if not all([total_chunks, file_type, file_id]):
            return JsonResponse({'success': False, 'error': 'Missing required parameters'}, status=400)
        
        if 'chunk' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No chunk file provided'}, status=400)
        
        # Define temp directory path
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', file_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save the chunk
        chunk_file = request.FILES['chunk']
        chunk_path = os.path.join(temp_dir, 'chunk_{}'.format(chunk_number))
        
        with open(chunk_path, 'wb+') as destination:
            for chunk in chunk_file.chunks():
                destination.write(chunk)
        
        # If this is the last chunk, combine all chunks
        if chunk_number == total_chunks - 1:
            # Create final file
            if file_type == 'image':
                final_path = os.path.join(settings.MEDIA_ROOT, 'missing_persons_images', '{}.jpg'.format(file_id))
            else:  # video
                final_path = os.path.join(settings.MEDIA_ROOT, 'missing_persons_videos', '{}.mp4'.format(file_id))
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            
            # Combine chunks
            with open(final_path, 'wb') as outfile:
                for i in range(total_chunks):
                    chunk_path = os.path.join(temp_dir, 'chunk_{}'.format(i))
                    if os.path.exists(chunk_path):
                        with open(chunk_path, 'rb') as infile:
                            outfile.write(infile.read())
            
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Create database record
            if file_type == 'image':
                relative_path = 'missing_persons_images/{}.jpg'.format(file_id)
                image = MissingPersonImage(
                    missing_person=missing_person,
                    image=relative_path
                )
                image.save()
                return JsonResponse({
                    'success': True,
                    'image_id': image.id,
                    'title': image.title,
                    'url': image.image.url
                })
            else:  # video
                relative_path = 'missing_persons_videos/{}.mp4'.format(file_id)
                video = RecordedVideo(
                    missing_person=missing_person,
                    video=relative_path
                )
                video.save()
                return JsonResponse({
                    'success': True,
                    'video_id': video.id,
                    'title': video.title,
                    'url': video.video.url
                })
        
        # If not the last chunk, return success for this chunk
        return JsonResponse({
            'success': True,
            'chunk_number': chunk_number,
            'chunks_received': chunk_number + 1,
            'total_chunks': total_chunks
        })
            
    except Exception as e:
        # Clean up any partial uploads in case of error
        if 'file_id' in locals() and file_id:
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', file_id)
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def add_live_url(request, person_id):
    """
    API endpoint to handle adding a live URL source.
    """
    try:
        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        # Try to parse the request body as JSON
        try:
            data = json.loads(request.body)
            url = data.get('url')
        except (ValueError, TypeError):
            # If not JSON, try form data
            url = request.POST.get('url')
        
        if not url:
            return JsonResponse({'success': False, 'errors': {'url': ['This field is required.']}}, status=400)
        
        # Create the live source
        live_source = LiveVideoSource(
            missing_person=missing_person,
            source_type='url',
            url=url
        )
        live_source.save()
        
        return JsonResponse({
            'success': True,
            'source_id': live_source.id,
            'title': live_source.title,
            'url': live_source.url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@login_required
@require_POST
def add_webcam_source(request, person_id):
    """
    API endpoint to handle adding a webcam source.
    """
    try:
        missing_person = get_object_or_404(MissingPerson, id=person_id, reported_by=request.user)
        
        # Create the webcam source
        live_source = LiveVideoSource(
            missing_person=missing_person,
            source_type='webcam',
            url="webcam://{}".format(uuid.uuid4())  # Generate a unique ID for this webcam source
        )
        live_source.save()
        
        return JsonResponse({
            'success': True,
            'source_id': live_source.id,
            'title': live_source.title
        })
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

@login_required
@require_POST
def delete_media(request):
    """
    API endpoint to delete uploaded media (image, video, or live source).
    """
    try:
        # Try to parse JSON body
        try:
            data = json.loads(request.body)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        
        media_type = data.get('media_type')
        media_id = data.get('media_id')
        
        if not media_type or not media_id:
            return JsonResponse({'success': False, 'error': 'Missing media_type or media_id'}, status=400)
        
        if media_type == 'image':
            item = get_object_or_404(MissingPersonImage, id=media_id, missing_person__reported_by=request.user)
        elif media_type == 'video':
            item = get_object_or_404(RecordedVideo, id=media_id, missing_person__reported_by=request.user)
        elif media_type == 'live':
            item = get_object_or_404(LiveVideoSource, id=media_id, missing_person__reported_by=request.user)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid media type'}, status=400)
        
        item.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500) 