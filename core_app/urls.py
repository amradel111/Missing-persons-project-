from django.urls import path

from core_app.views import placeholder
from core_app.views.dashboard_views import dashboard_view
from core_app.views.api_views import (
    get_missing_person, delete_missing_person,
    get_missing_person_images, get_missing_person_videos, get_missing_person_live_sources
)
from core_app.views.upload_views import (
    upload_media_page, upload_person_image, upload_recorded_video,
    add_live_url, add_webcam_source, delete_media, upload_chunk
)
from core_app.views.search_views import live_search_page, log_match_view, live_search_redirect

app_name = 'core_app'

urlpatterns = [
    # Health check endpoint
    path('health/', placeholder, name='health_check'),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Upload Media Page
    path('upload-media/', upload_media_page, name='upload_media'),
    
    # Media Upload API endpoints
    path('api/missing-persons/<int:person_id>/images/upload/', upload_person_image, name='upload_person_image'),
    path('api/missing-persons/<int:person_id>/videos/upload/', upload_recorded_video, name='upload_recorded_video'),
    path('api/missing-persons/<int:person_id>/chunk/upload/', upload_chunk, name='upload_chunk'),
    path('api/missing-persons/<int:person_id>/live-url/add/', add_live_url, name='add_live_url'),
    path('api/missing-persons/<int:person_id>/webcam/add/', add_webcam_source, name='add_webcam_source'),
    path('api/media/delete/', delete_media, name='delete_media'),
    
    # Media Fetch API endpoints
    path('api/missing-persons/<int:person_id>/images/', get_missing_person_images, name='get_missing_person_images'),
    path('api/missing-persons/<int:person_id>/videos/', get_missing_person_videos, name='get_missing_person_videos'),
    path('api/missing-persons/<int:person_id>/live-sources/', get_missing_person_live_sources, name='get_missing_person_live_sources'),
    
    # API endpoints
    path('api/missing-persons/<int:person_id>/', get_missing_person, name='get_missing_person'),
    path('api/matches/log/', log_match_view, name='log_match'),
    
    # Missing person profiles management
    path('missing-persons/<int:person_id>/delete/', delete_missing_person, name='delete_missing_person'),

    # Live Search Pages
    path('search/live/person/<int:person_id>/source/<int:source_id>/', live_search_page, name='live_search_page'),
    path('live-search-redirect/', live_search_redirect, name='live_search_redirect'),
]
