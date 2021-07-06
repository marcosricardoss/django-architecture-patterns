from crontab import CronTab

from django.conf import settings
from django.core.management import call_command

from django_crontab.crontab import Crontab


def get_cronjob_from_settings():
    result = {}
    settings_cronjobs = getattr(settings, "CRONJOBS", [])
    for job in settings_cronjobs:
        jobhash = Crontab()._Crontab__hash_job(job)
        result[jobhash] = job

    return result


def get_cronjob_running():
    result = {}
    cron = CronTab(user="root")
    for jobhash, cronjob in get_cronjob_from_settings().items():
        for job in cron:
            if jobhash in job.command:
                result[jobhash] = {"command": job.command, "setting": cronjob}

    return result


def run_cronjob(jobhash):
    call_command("crontab", "run", jobhash)


def add_all_cronjobs():
    call_command("crontab", "add")


def remove_all_cronjobs():
    call_command("crontab", "remove")
