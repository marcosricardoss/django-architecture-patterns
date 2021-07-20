import pytest

from django.db import IntegrityError

from task.models import Task
from task.services import unit_of_work, add_task_service
from task.services.exceptions import TaskException


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __enter__(self):
        self.committed = False
        self.rollbacked = False

    def __exit__(self, *args):
        self.committed = True
        self.rollbacked = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rollbacked = True


def test_add_batch(dates, monkeypatch):
    def save(*args, **kwargs):
        return

    monkeypatch.setattr(Task, "save", save)
    uow = FakeUnitOfWork()
    add_task_service(
        title="Task Title",
        description="Task Description",
        deadline_at=dates["tomorrow"],
        finished_at=dates["tomorrow"],
        uow=uow,
    )


def test_add_batch_with_exception(dates, monkeypatch):
    def save(*args, **kwargs):
        raise IntegrityError()

    monkeypatch.setattr(Task, "save", save)
    uow = FakeUnitOfWork()
    with pytest.raises(TaskException):
        add_task_service(
            title="Task Title",
            description="Task Description",
            deadline_at=dates["tomorrow"],
            finished_at=dates["tomorrow"],
            uow=uow,
        )
    uow.committed = False
