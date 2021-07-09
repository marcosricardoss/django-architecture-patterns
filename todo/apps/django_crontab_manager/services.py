import logging

from crontab import CronTab

from django.conf import settings
from django.core.management import call_command

from django_crontab.crontab import Crontab

from .models import Cronjob
from .app_settings import CRONJOBS

logger = logging.getLogger("django")

def get_cronjob_from_settings():
    result = {}   
    for job in CRONJOBS:
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

def load_cronjobs_to_db():    
    Cronjob.objects.all().delete()
    for jobhash, cronjob in get_cronjob_from_settings().items():        
        Cronjob.objects.get_or_create(jobhash=jobhash, setting=cronjob)
    
def debugger_cronjob():
    logger.info(f"Running debugger cronjob...")