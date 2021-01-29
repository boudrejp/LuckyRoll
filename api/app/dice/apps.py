from django.apps import AppConfig


class DiceConfig(AppConfig):
    name = 'dice'

    def ready(self):
        import dice.signals