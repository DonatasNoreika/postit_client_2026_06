from django.apps import AppConfig


class PostitClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postit_client'

    def ready(self):
        from .signals import create_profile, save_profile
