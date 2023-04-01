from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = 'main'

    def ready(self):
        print("READY FUNCTION")
        from . import updater
        updater.start()
