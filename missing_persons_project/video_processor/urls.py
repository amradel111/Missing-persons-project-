from django.urls import path

from core_app.views import placeholder

app_name = 'video_processor'

urlpatterns = [
    # URLs will be added as views are implemented
    path('status/', placeholder, name='video_status'),
]
