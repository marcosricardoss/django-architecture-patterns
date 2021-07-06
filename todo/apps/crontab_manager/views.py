from django import template
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View

from .services import (
    get_cronjob_from_settings,
    get_cronjob_running,
    run_cronjob,
    add_all_cronjobs,
    remove_all_cronjobs,
)

register = template.Library()


class CronJobHomeView(View):
    template_name = "crontab_manager/home.html"

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
        return HttpResponseRedirect(reverse("crontab_manager:home"))


class AddAllCronJobsView(View):
    def get(self, request, *args, **kwargs):
        add_all_cronjobs()
        messages.success(self.request, f"All cronjobs were removed from execution successfully!")
        return HttpResponseRedirect(reverse("crontab_manager:home"))


class RemoveAllCronJobsView(View):
    def get(self, request, *args, **kwargs):
        remove_all_cronjobs()
        messages.success(self.request, f"All cronjobs were removed successfully!")
        return HttpResponseRedirect(reverse("crontab_manager:home"))
