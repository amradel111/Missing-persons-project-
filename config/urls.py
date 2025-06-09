"""Main URL Configuration for Missing Persons Finder project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Simple redirection to login page
def home_view(request):
    return redirect('user_auth:login')

urlpatterns = [
    # Home URL redirects to login
    path('', home_view, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # App URLs - Web pages
    path('', include('core_app.urls')),  # Mount core_app URLs at root for web pages
    path('auth/', include('user_auth.urls')),
]

# Add debug toolbar if in development
if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
