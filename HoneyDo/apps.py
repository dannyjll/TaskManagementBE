from django.apps import AppConfig


class HoneydoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HoneyDo'

    def ready(self):
        import HoneyDo.signals  # noqa