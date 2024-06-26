from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaskConfig(AppConfig):
    name = "task"
    verbose_name = _("Task")

    def ready(self):
        from . import signals
