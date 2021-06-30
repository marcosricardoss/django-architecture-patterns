import pytest

from django.db.utils import IntegrityError

from task.models import Task


@pytest.mark.django_db
def test_task_create(dates):

    task = Task(
        title="Task Name",
        description="Task description",
        deadline_at=dates["later"],
        finished_at=dates["tomorrow"],
    )
    task.save()
    assert task.id
    assert task.title == "Task Name"
    assert task.description == "Task description"
    assert task.deadline_at == dates["later"]
    assert task.finished_at == dates["tomorrow"]
    assert task.created_at >= dates["today"]
    assert task.updated_at >= dates["today"]
    assert not task.is_past_due
    assert task.get_absolute_url() == f"/detail/{task.id}/"
    assert str(task) == "Task Name"


@pytest.mark.django_db
def test_task_create_with_tags(dates):
    task = Task(
        title="Task Name",
        description="Task description",
        deadline_at=dates["later"],
        finished_at=dates["tomorrow"],
    )
    task.save()
    task.tags.create(slug="tag-slug-1")
    task.tags.create(slug="tag-slug-2")

    assert task.id
    assert task.title == "Task Name"
    assert task.description == "Task description"
    assert task.deadline_at == dates["later"]
    assert task.finished_at == dates["tomorrow"]
    assert task.created_at >= dates["today"]
    assert task.updated_at >= dates["today"]
    assert not task.is_past_due
    assert task.get_absolute_url() == f"/detail/{task.id}/"
    assert task.tag_list[0].slug == "tag-slug-1"
    assert task.tag_list[1].slug == "tag-slug-2"
    assert str(task) == "Task Name"


@pytest.mark.django_db
def test_task_create_without_not_null_field():
    task = Task()
    with pytest.raises(IntegrityError):
        task.save()


@pytest.mark.django_db
def test_task_create_with_past_due_equal_to_true(dates):

    task = Task(
        title="Task Name",
        description="Task description",
        deadline_at=dates["tomorrow"],
        finished_at=dates["later"],
    )
    task.save()
    assert task.is_past_due
