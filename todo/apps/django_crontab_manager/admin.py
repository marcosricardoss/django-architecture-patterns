import logging

from django.contrib import admin, messages

from .adapters import DjangoExecutor
from .models import Cronjob
from .services import run_cronjob, get_cronjob_running

logger = logging.getLogger("django")


def run_action(modeladmin, request, queryset):
    logger.info(f"HttpRequest.method: {request.method}...")    
    for e in queryset:
        run_cronjob(e.jobhash, DjangoExecutor())
        logger.info(f"Running cronjob: {e.jobhash}...")
        messages.success(request, f"Running cronjobs: {e.jobhash}")

run_action.short_description = "Run selected cronjobs"


class CronjobModelAdmin(admin.ModelAdmin):
    model = Cronjob
    #change_form_template = "django_crontab_manager/admin_cronjob_change_form.html"
    change_list_template = "django_crontab_manager/admin_cronjob_changelist.html"
    list_display = ['jobhash', 'setting', "is_running"]
    actions = [run_action]

    #def response_change(self, request, obj):
    #    if "_make-unique" in request.POST:
    #        logger.info(f"Running cronjob: {obj.jobhash}...")
    #        self.message_user(request, "This villain is now unique")            
    #    return super().response_change(request, obj)        

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def is_running(self, obj):
        return obj.jobhash in get_cronjob_running()

    is_running.allow_tags = True
    is_running.short_description = 'Running on Cron'


admin.site.register(Cronjob, CronjobModelAdmin)
