from django.apps import AppConfig


class DjangoCrontabManagerConfig(AppConfig):
    name = 'django_crontab_manager'
    verbose_name = 'Crontab Manager'

    def ready(self):
        try:
            from .services import load_cronjobs_to_db
            load_cronjobs_to_db()
        except:
            pass
