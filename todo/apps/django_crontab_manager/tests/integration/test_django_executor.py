from crontab import CronTab
from django_crontab.crontab import Crontab
from django_crontab_manager.adapters import DjangoExecutor


def test_django_django_executor_adding_jobs_to_cron():
    job = ("*/1 * * * *", "django_crontab_manager.services.debugger_cronjob")
    jobhash = Crontab()._Crontab__hash_job(job)

    executor = DjangoExecutor()
    executor.run(["crontab", "add"])
    
    cron = CronTab(user="root")
    assert [job for job in cron if jobhash in job.command]


def test_django_django_executor_removing_jobs_to_cron():
    job = ("*/1 * * * *", "django_crontab_manager.services.debugger_cronjob")
    jobhash = Crontab()._Crontab__hash_job(job)

    executor = DjangoExecutor()
    executor.run(["crontab", "remove"])
    
    cron = CronTab(user="root")
    assert not [job for job in cron if jobhash in job.command]
