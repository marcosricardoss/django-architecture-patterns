import pytest
from django.utils.dateparse import parse_datetime

from django_crontab_manager.models import Cronjob
from django_crontab_manager.adapters import (
    DjangoRepository,
    CronjobRepository
)


@pytest.mark.django_db
def test_django_repository_instantiation():
    cronjob_repository = DjangoRepository(Cronjob)
    assert cronjob_repository.model == Cronjob


@pytest.mark.django_db
def test_cronjob_repository_can_retrieve_a_job():
    cronjob = CronjobRepository().get(id=1)
    assert cronjob.id == 1
    assert cronjob.jobhash == "08632410ed34932a99a3505eb24e6390"
    assert cronjob.setting == "('*/1 * * * *', 'example.services.my_scheduled_job_1')"
    assert cronjob.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert cronjob.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")


@pytest.mark.django_db
def test_cronjob_repository_can_retrieve_all_jobs():
    cronjobs = CronjobRepository().list()
    assert len(cronjobs) == 3

    cronjob = cronjobs[0]
    assert cronjob.id == 1
    assert cronjob.jobhash == "08632410ed34932a99a3505eb24e6390"
    assert cronjob.setting == "('*/1 * * * *', 'example.services.my_scheduled_job_1')"
    assert cronjob.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert cronjob.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")

    cronjob = cronjobs[1]
    assert cronjob.id == 2
    assert cronjob.jobhash == "195982eae0c445a847832183b9b4c24e"
    assert cronjob.setting == "('*/1 * * * *', 'example.services.my_scheduled_job_2')"
    assert cronjob.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert cronjob.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")

    cronjob = cronjobs[2]
    assert cronjob.id == 3
    assert cronjob.jobhash == "94861d9b3515af808030afe2a164a48f"
    assert cronjob.setting == "('*/1 * * * *', 'example.services.my_scheduled_job_3')"
    assert cronjob.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert cronjob.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")


@pytest.mark.django_db
def test_cronjob_repository_can_delete_all_jobs():
    CronjobRepository().delete()
    cronjobs = CronjobRepository().list()
    assert not cronjobs


@pytest.mark.django_db
def test_cronjob_repository_can_create_a_job():
    cronjob = CronjobRepository().create(
        jobhash="xxxxxxxxxxxxxxx",
        setting="('*/1 * * * *', 'example.services.my_scheduled_job')"
    )
    cronjob.id == 4
    cronjob.jobhash="xxxxxxxxxxxxxxx",
    cronjob.setting="('*/1 * * * *', 'example.services.my_scheduled_job')"
    assert cronjob.created_at
    assert cronjob.updated_at
