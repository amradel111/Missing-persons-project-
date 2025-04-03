from django.urls import path

from core_app.views import placeholder

app_name = 'core_app'

urlpatterns = [
    # URLs will be added as views are implemented
    path('health/', placeholder, name='health_check'),
]
