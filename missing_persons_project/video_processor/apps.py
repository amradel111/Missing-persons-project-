from django.apps import AppConfig


class VideoProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_processor'
    verbose_name = 'Video Processor'

    def ready(self):
        """Initialize any signals or startup tasks."""
        pass
