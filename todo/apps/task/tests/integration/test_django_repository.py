import pytest
from django.utils.dateparse import parse_datetime

from task.models import Task
from task.exceptions import (
    CreateObjectException,
    UpdateObjectException,
    ObjectDoesNotExist,
)
from task.adapters import DjangoRepository


@pytest.mark.django_db
def test_django_repository_instantiation():
    task_repository = DjangoRepository(Task)
    assert task_repository.model == Task


@pytest.mark.django_db
def test_django_repository_can_create_a_job(dates):
    tomorrow = dates["tomorrow"]
    title = "Do Something"
    description = "Something description"
    deadline_at = tomorrow
    finished_at = tomorrow
    task = DjangoRepository(Task).create(
        data={
            "title": title,
            "description": description,
            "deadline_at": deadline_at,
            "finished_at": finished_at,
        }
    )
    assert task.id
    assert task.title == title
    assert task.description == description
    assert task.deadline_at == deadline_at
    assert task.finished_at == finished_at
    assert task.created_at
    assert task.updated_at


@pytest.mark.django_db
def test_django_repository_try_create_a_object_without_defaults_values():
    with pytest.raises(CreateObjectException):
        DjangoRepository(Task).create(
            data={
                "title": None,
                "description": None,
                "deadline_at": None,
                "finished_at": None,
            }
        )


@pytest.mark.django_db
def test_django_repository_can_retrieve_a_object():
    task = DjangoRepository(Task).get(id=1)
    assert task.id == 1
    assert task.title == "Task Name 1"
    assert task.description == "Task description 1"
    assert task.deadline_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.finished_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.tag_list[0].slug == "tag-1"
    assert task.tag_list[0].created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.tag_list[0].created_at == parse_datetime("2021-10-20T20:00:00.000Z")


@pytest.mark.django_db
def test_django_repository_retrieving_a_nonexistent_object():
    with pytest.raises(ObjectDoesNotExist):
        DjangoRepository(Task).get(id="99999")


@pytest.mark.django_db
def test_django_repository_can_update_a_object(dates):
    task = DjangoRepository(Task).get(id=1)
    title = "Do Something Edited"
    description = "Something description Edited"
    deadline_at = dates["later"]
    finished_at = dates["tomorrow"]
    task = DjangoRepository(Task).update(
        task.id,
        data={
            "title": title,
            "description": description,
            "deadline_at": deadline_at,
            "finished_at": finished_at,
        },
    )
    assert task.id
    assert task.title == title
    assert task.description == description
    assert task.deadline_at == deadline_at
    assert task.finished_at == finished_at
    assert task.created_at
    assert task.updated_at


@pytest.mark.django_db
def test_django_repository_try_update_a_object_without_defaults_values():
    task = DjangoRepository(Task).get(id=1)
    with pytest.raises(UpdateObjectException):
        DjangoRepository(Task).update(
            task.id,
            data={
                "title": None,
                "description": None,
                "deadline_at": None,
                "finished_at": None,
            }
        )


@pytest.mark.django_db
def test_django_repository_delete_a_object():
    repository = DjangoRepository(Task)
    id = repository.get(1).id
    repository.delete(id)    
    with pytest.raises(ObjectDoesNotExist):
        assert repository.get(1)
    


@pytest.mark.django_db
def test_django_repository_can_retrieve_all_object():
    tasks = DjangoRepository(Task).list()
    assert len(tasks) == 10
    task = tasks[0]
    assert task.id == 1
    assert task.title == "Task Name 1"
    assert task.description == "Task description 1"
    assert task.deadline_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.finished_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.updated_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.tag_list[0].slug == "tag-1"
    assert task.tag_list[0].created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert task.tag_list[0].created_at == parse_datetime("2021-10-20T20:00:00.000Z")
