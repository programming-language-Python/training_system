from django.apps import AppConfig


class BaseTestingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.base_testing'
