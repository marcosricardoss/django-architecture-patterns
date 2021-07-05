from task.models import Tag
from .repository import DjangoRepository


class TagRepository(DjangoRepository):
    def __init__(self) -> None:
        super().__init__(Tag)
