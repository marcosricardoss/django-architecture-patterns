import pytest

from task.models import Task
from task.adapters import TaskRepository


@pytest.mark.django_db
def test_django_task_repository_instantiation():
    repository = TaskRepository()
    assert repository.model == Task