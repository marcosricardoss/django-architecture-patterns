import pytest

from django.db.utils import IntegrityError

from task.models import Tag


@pytest.mark.django_db
def test_task_create():

    tag = Tag(
        slug="tag-slug",
    )
    tag.save()
    assert tag.id
    assert tag.slug == "tag-slug"
    assert tag.get_absolute_url() == f"/detail/{tag.id}/"
    assert str(tag) == "tag-slug"


@pytest.mark.django_db
def test_tag_create_without_not_null_field():
    tag = Tag(slug=None)
    with pytest.raises(IntegrityError):
        tag.save()
