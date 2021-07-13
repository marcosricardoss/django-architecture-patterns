import pytest

from django.db.utils import IntegrityError

from django_crontab_manager.models import Cronjob


@pytest.mark.django_db
def test_task_cronjob(dates):

    cronjob = Cronjob(
        jobhash="xxxxxxxxxxxxxxxxxxxxxx",
        setting="('*/1 * * * *', 'example.services.my_scheduled_job')",
    )
    cronjob.save()
    assert cronjob.id
    assert cronjob.jobhash == "xxxxxxxxxxxxxxxxxxxxxx"
    assert cronjob.setting == "('*/1 * * * *', 'example.services.my_scheduled_job')"
    assert cronjob.created_at >= dates["today"]
    assert cronjob.updated_at >= dates["today"]
    assert str(cronjob) == cronjob.setting


@pytest.mark.django_db
def test_cronjob_create_without_not_null_field():
    cronjob = Cronjob(jobhash=None, setting=None)
    with pytest.raises(IntegrityError):
        cronjob.save()


@pytest.mark.django_db
def test_cronjob_create_with_jobhash_already_used():
    # cronjob 1
    cronjob1 = Cronjob(
        jobhash="xxxxxxxxxxxxxxxxxxxxxx",
        setting="('*/1 * * * *', 'example.services.my_scheduled_job')",
    )
    cronjob1.save()
    # cronjob 2
    cronjob2 = Cronjob(
        jobhash="xxxxxxxxxxxxxxxxxxxxxx",  # the same jobash of cronjob1
        setting="('*/0 * * * *', 'example.services.my_scheduled_job')",
    )
    with pytest.raises(IntegrityError):
        cronjob2.save()
