from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authorization"

    def ready(self):
        # required to import signals
        import authorization.signals  # noqa
