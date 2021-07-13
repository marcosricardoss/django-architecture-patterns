from django_crontab.crontab import Crontab

from django_crontab_manager.adapters import DjangoExecutor
from django_crontab_manager.services import add_all_cronjobs


def test_run_cronjob_view(admin_client):
    add_all_cronjobs(DjangoExecutor())

    job = ("*/1 * * * *", "django_crontab_manager.services.debugger_cronjob")
    jobhash = Crontab()._Crontab__hash_job(job)

    response = admin_client.get(f"/crontab_manager/run/{jobhash}/", follow=True)
    assert response.status_code == 200
    assert response.content.count(b"Success!") == 1
    assert response.content.count(f"Running the {jobhash} cronjob".encode()) == 1    
    assert response.content.count(b"Reload") == 1
    assert response.content.count(b"Remove All") == 1


def test_run_cronjob_admin_view(admin_client):
    job = ("*/1 * * * *", "django_crontab_manager.services.debugger_cronjob")
    jobhash = Crontab()._Crontab__hash_job(job)

    response = admin_client.get(f"/crontab_manager/run-admin/{jobhash}/", follow=True)
    assert response.status_code == 200
    assert response.content.count(f"Running the {jobhash} cronjob".encode()) == 1


def test_access_add_all_cronjobs_view_without_being_logged_as_admin_user(client):
    job = ("*/1 * * * *", "django_crontab_manager.services.debugger_cronjob")
    jobhash = Crontab()._Crontab__hash_job(job)
    response = client.get(f"/crontab_manager/run/{jobhash}/")
    assert response.status_code == 302
