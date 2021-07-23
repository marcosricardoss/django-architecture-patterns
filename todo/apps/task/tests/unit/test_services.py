from dataclasses import dataclass

from django.utils import timezone

from task.services import unit_of_work
from task.adapters import AbstractRepository
from task.services import add_task_service, update_task_service, detele_task_service


@dataclass
class FakeModel:
    updated_at: timezone = timezone.now()


class FakeRepository(AbstractRepository):
    def __init__(self) -> None:
        self.deleted = False
        self.data = {}
        self.object_id = None

    def create(self, data):
        self.data = data.values()

    def get(self, id):
        pass

    def update(self, id, data):
        self.object_id = id
        self.data = data.values()
        return FakeModel()

    def delete(self, id):
        self.object_id = id

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


def test_add_task_service(dates):    
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
    assert title in repository.data
    assert description in repository.data
    assert deadline_at in repository.data
    assert finished_at in repository.data
    assert uow.committed == True
    assert uow.rollbacked == False


def test_add_update_service(dates):    
    id = 20
    title = "Task Title"
    description = "Task Description"
    deadline_at = dates["later"]
    finished_at = dates["tomorrow"]
    repository = FakeRepository()
    uow = FakeUnitOfWork()
    update_task_service(
        id=id,
        title=title,
        description=description,
        deadline_at=deadline_at,
        finished_at=finished_at,
        repository=repository,
        uow=uow,
    )
    assert repository.object_id == id
    assert title in repository.data
    assert description in repository.data
    assert deadline_at in repository.data
    assert finished_at in repository.data
    assert uow.committed == True
    assert uow.rollbacked == False


def test_detele_task_service():
    id = 20
    repository = FakeRepository()
    uow = FakeUnitOfWork()
    detele_task_service(
        id=id,
        repository=repository,
        uow=uow,
    )
    assert repository.object_id == id
    assert uow.committed == True
    assert uow.rollbacked == False

