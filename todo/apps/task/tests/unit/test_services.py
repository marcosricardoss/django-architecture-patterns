import pytest

from django.db import IntegrityError

from task.models import Task
from task.services import unit_of_work
from task.adapters import AbstractRepository
from task.exceptions import CreateObjectException
from task.services import add_task_service


class FakeRepository(AbstractRepository):
    def __init__(self) -> None:
        self.deleted = False
        self.created_data = {}

    def create(self, data):
        self.created_data = data.values()

    def get(self, id):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def list(self):
        pass


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


def test_add_task(dates):    
    title = "Task Title"
    description = "Task Description"
    deadline_at = dates["later"]
    finished_at = dates["tomorrow"]
    repository = FakeRepository()
    uow = FakeUnitOfWork()
    add_task_service(
        title=title,
        description=description,
        deadline_at=deadline_at,
        finished_at=finished_at,
        repository=repository,
        uow=uow,
    )
    assert title in repository.created_data
    assert description in repository.created_data
    assert deadline_at in repository.created_data
    assert finished_at in repository.created_data
    assert uow.committed == True
    assert uow.rollbacked == False
