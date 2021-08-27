import pytest

from task.models import Tag
from task.adapters import TagRepository


@pytest.mark.django_db
def test_django_tag_repository_instantiation():
    repository = TagRepository()
    assert repository.model == Tag