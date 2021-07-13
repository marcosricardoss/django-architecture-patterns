from crontab import CronTab

from django_crontab_manager.adapters import DjangoExecutor
from django_crontab_manager.services import (
    add_all_cronjobs,
    get_cronjob_from_settings,
    remove_all_cronjobs,
)


def test_view_page_running_all_jobs(admin_client):
    add_all_cronjobs(DjangoExecutor())
    response = admin_client.get("/crontab_manager/")
    assert response.status_code == 200
    assert response.content.count(b"Reload") == 1
    assert response.content.count(b"Remove All") == 1

    # jobs running
    cron = CronTab(user="root")
    for job in cron:
        assert response.content.count(job.command.encode()) == 1


def test_home_view_with_running_any_jobs(admin_client):
    remove_all_cronjobs(DjangoExecutor())
    response = admin_client.get("/crontab_manager/")
    assert response.status_code == 200
    assert response.content.count(b"Run All") == 1
    assert response.content.count(b"Remove All") == 1

    # job from settings
    for jobhash, _ in get_cronjob_from_settings().items():
        assert response.content.count(jobhash.encode()) == 1

    # no running job
    cron = CronTab(user="root")
    for job in cron:
        assert response.content.count(job.command.encode()) == 0


def test_access_home_view_without_being_logged_as_admin_user(client):
    remove_all_cronjobs(DjangoExecutor())
    response = client.get("/crontab_manager/")
    assert response.status_code == 302
