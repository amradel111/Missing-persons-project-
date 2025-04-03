from django.urls import path

from core_app.views import placeholder

app_name = 'search_manager'

urlpatterns = [
    # URLs will be added as views are implemented
    path('status/', placeholder, name='search_status'),
]
