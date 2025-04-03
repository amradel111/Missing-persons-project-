from django.apps import AppConfig


class SearchManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_manager'
    verbose_name = 'Search Manager'

    def ready(self):
        """Initialize any signals or startup tasks."""
        pass
