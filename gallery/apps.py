from django.apps import AppConfig

class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gallery'

    def ready(self):
        import gallery.signals  # Importáld a signals.py-t