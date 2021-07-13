import logging

from crontab import CronTab

from django_crontab.crontab import Crontab

from .app_settings import CRONJOBS
from .adapters import AbstractRepository, AbstractExecutor

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


def run_cronjob(jobhash, executor: AbstractExecutor):
    executor.run(["crontab", "run", jobhash])


def add_all_cronjobs(executor: AbstractExecutor):
    executor.run(["crontab", "add"])


def remove_all_cronjobs(executor: AbstractExecutor):
    executor.run(["crontab", "remove"])


def load_cronjobs_to_db(cronjob_repository: AbstractRepository):
    cronjob_repository.delete()
    for jobhash, cronjob in cronjob_repository.list():
        cronjob_repository.create(jobhash, cronjob)


def debugger_cronjob(): # pragma: no cover
    logger.info(f"Running debugger cronjob...")
