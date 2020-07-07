from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'
    def ready():
        from . import signals
