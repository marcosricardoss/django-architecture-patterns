from django.contrib import messages
from django.shortcuts import Http404, HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views import View

from .services import (
    get_cronjob_from_settings,
    get_cronjob_running,
    run_cronjob,
    add_all_cronjobs,
    remove_all_cronjobs,
)


class CronJobHomeView(View):

    template_name = "django_crontab_manager/home.html"

    def get(self, request, *args, **kwargs):        
        view_context = {
            "settings_cronjobs": get_cronjob_from_settings(),
            "running_cronjobs": get_cronjob_running(),
        }
        return render(request, self.template_name, view_context)


class RunCronJobView(View):
    def get(self, request, *args, **kwargs):
        jobhash = self.kwargs.get("jobhash")
        run_cronjob(jobhash)
        messages.success(self.request, f"Running the {jobhash} cronjob")
        return HttpResponseRedirect(reverse("django_crontab_manager:home"))


class RunCronJobAdminView(View):
    def get(self, request, *args, **kwargs):
        jobhash = self.kwargs.get("jobhash")
        run_cronjob(jobhash)
        messages.success(self.request, f"Running the {jobhash} cronjob")
        return HttpResponseRedirect(
            reverse("admin:django_crontab_manager_cronjob_changelist")
        )


class AddAllCronJobsView(View):
    def get(self, request, *args, **kwargs):
        add_all_cronjobs()
        messages.success(
            self.request, f"All cronjobs were removed from execution successfully!"
        )
        return HttpResponseRedirect(reverse("django_crontab_manager:home"))


class AddAllCronJobsAdminView(View):
    def get(self, request, *args, **kwargs):
        add_all_cronjobs()
        messages.success(
            self.request, f"All cronjobs were removed from execution successfully!"
        )
        return HttpResponseRedirect(
            reverse("admin:django_crontab_manager_cronjob_changelist")
        )


class RemoveAllCronJobsView(View):
    def get(self, request, *args, **kwargs):
        remove_all_cronjobs()
        messages.success(self.request, f"All cronjobs were removed successfully!")
        return HttpResponseRedirect(reverse("django_crontab_manager:home"))


class RemoveAllCronJobsAdminView(View):
    def get(self, request, *args, **kwargs):
        remove_all_cronjobs()
        messages.success(self.request, f"All cronjobs were removed successfully!")
        return HttpResponseRedirect(
            reverse("admin:django_crontab_manager_cronjob_changelist")
        )
