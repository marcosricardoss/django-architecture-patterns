from django.conf import settings

CRONJOBS = getattr(settings, "CRONJOBS", [])
DEBUG = getattr(settings, "DEBUG", False)
if DEBUG:
    CRONJOBS.append(('*/1 * * * *', 'django_crontab_manager.services.debugger_cronjob'))