import os
from pathlib import Path

# Define the project root
PROJECT_ROOT = Path("missing_persons_project")

# Create project structure
dirs = [
    # Core app
    "core_app/models",
    "core_app/views",
    "core_app/serializers",
    "core_app/templates",
    "core_app/utils",
    
    # User auth
    "user_auth/models",
    "user_auth/views",
    "user_auth/templates",
    
    # Search manager
    "search_manager/models",
    "search_manager/views",
    "search_manager/serializers",
    "search_manager/utils",
    
    # Video processor
    "video_processor/models",
    "video_processor/views",
    "video_processor/serializers",
    "video_processor/services",
    
    # Config structure
    "config/settings",
    
    # Other directories
    "tests",
    "static",
    "media",
]

# Create directories
for directory in dirs:
    os.makedirs(PROJECT_ROOT / directory, exist_ok=True)
    # Create an __init__.py file in each directory to make it a proper Python package
    with open(PROJECT_ROOT / directory / "__init__.py", "w") as f:
        pass

# Create required files
files = [
    # Core app
    "core_app/urls.py",
    "core_app/__init__.py",
    "core_app/apps.py",
    
    # User auth
    "user_auth/urls.py",
    "user_auth/__init__.py",
    "user_auth/apps.py",
    "user_auth/forms.py",
    
    # Search manager
    "search_manager/urls.py",
    "search_manager/__init__.py",
    "search_manager/apps.py",
    
    # Video processor
    "video_processor/urls.py",
    "video_processor/__init__.py",
    "video_processor/apps.py",
    
    # Config files
    "config/__init__.py",
    "config/urls.py",
    "config/wsgi.py",
    "config/asgi.py",
    "config/settings/__init__.py",
    "config/settings/base.py",
    "config/settings/development.py",
    "config/settings/production.py",
    
    # Manage.py
    "manage.py",
    
    # .env file
    ".env",
]

for file_path in files:
    with open(PROJECT_ROOT / file_path, "w") as f:
        pass

print("Project structure created successfully!") 