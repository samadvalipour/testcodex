from django.apps import AppConfig


class ActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activity'
    def ready(self):
        from actstream import registry
        registry.register(self.get_model('ActivityTargets'))
