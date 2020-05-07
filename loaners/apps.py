from django.apps import AppConfig


class LoanersConfig(AppConfig):
    name = 'loaners'

    def ready(self):
        import loaners.signals