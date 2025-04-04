from django.urls import path

from core_app.views import placeholder
from core_app.views.dashboard_views import dashboard_view
from core_app.views.api_views import get_missing_person, delete_missing_person

app_name = 'core_app'

urlpatterns = [
    # Health check endpoint
    path('health/', placeholder, name='health_check'),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # API endpoints
    path('api/missing-persons/<int:person_id>/', get_missing_person, name='get_missing_person'),
    
    # Missing person profiles management
    path('missing-persons/<int:person_id>/delete/', delete_missing_person, name='delete_missing_person'),
]
