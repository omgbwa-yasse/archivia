from django.apps import AppConfig

class IntelligenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intelligence'
    verbose_name = 'Intelligence'
    verbose_name_plural = 'Intelligence'

    def ready(self):
        import intelligence.signals  # noqa 