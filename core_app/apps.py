from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_app'
    verbose_name = 'Core Application'

    def ready(self):
        """Initialize any signals or startup tasks."""
        pass
