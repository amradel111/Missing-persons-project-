"""Main URL Configuration for Missing Persons Finder project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
from django.shortcuts import redirect

# Simple redirection to login page
def home_view(request):
    return redirect('user_auth:login')

# Create schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Missing Persons Finder API",
        default_version='v1',
        description="API documentation for Missing Persons Finder application",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Home URL redirects to login
    path('', home_view, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # App URLs - API endpoints
    path('api/core/', include('core_app.urls')),
    path('api/auth/', include('user_auth.urls')),
    path('api/search/', include('search_manager.urls')),
    path('api/video/', include('video_processor.urls')),
    
    # App URLs - Web pages
    path('', include('core_app.urls')),  # Mount core_app URLs at root for web pages
]

# Add debug toolbar if in development
if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
