from django.apps import AppConfig

class FinanzasConfig(AppConfig):
    name = "applications.finanzas"

    def ready(self):
        import applications.finanzas.signals