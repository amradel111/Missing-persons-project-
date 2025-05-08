"""
Development settings for Missing Persons Finder project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# For Swagger documentation in development
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}

# Use console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Remove debug toolbar for now
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Override the DATABASES setting from base.py to use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Use PostgreSQL as the database backend
        'NAME': 'myproject',         # Replace with your actual PostgreSQL database name
        'USER': 'postgres',          # Using the default PostgreSQL superuser; change if needed
        'PASSWORD': '33445566',  # Replace with your actual PostgreSQL password
        'HOST': 'localhost',         # For local PostgreSQL
        'PORT': '5432',              # Default PostgreSQL port
    }
}
