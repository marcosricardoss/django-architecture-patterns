import pytest
from django.utils.dateparse import parse_datetime

from task.models import Task, Tag
from task.repositories import DjangoRepository, TagRepository, TaskRepository


@pytest.mark.django_db
def test_django_repository_instantiation():
    task_repository = DjangoRepository(Task)
    tag_repository = DjangoRepository(Tag)
    assert task_repository.model == Task
    assert tag_repository.model == Tag


@pytest.mark.django_db
def test_task_repository_can_retrieve_a_task():
    task = TaskRepository().get(id=1)
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
def test_task_repository_can_retrieve_all_task():
    tasks = TaskRepository().list()
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


@pytest.mark.django_db
def test_tag_repository_can_retrieve_a_tag():
    tag = TagRepository().get(id=1)
    assert tag.id == 1
    assert tag.slug == "tag-1"
    assert tag.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert tag.created_at == parse_datetime("2021-10-20T20:00:00.000Z")


@pytest.mark.django_db
def test_tag_repository_can_retrieve_all_tags():
    tags = TagRepository().list()
    tag = tags[0]
    assert tag.id == 1
    assert tag.slug == "tag-1"
    assert tag.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
    assert tag.created_at == parse_datetime("2021-10-20T20:00:00.000Z")
