from django.apps import AppConfig


class News3Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news3'

    def ready(self):
        import news3.signals
