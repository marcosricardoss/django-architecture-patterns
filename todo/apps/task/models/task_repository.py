from .task import Task
from .repository import DjangoRepository


class TaskRepository(DjangoRepository):
    def __init__(self) -> None:
        super().__init__(Task)
