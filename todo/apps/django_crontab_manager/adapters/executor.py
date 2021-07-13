import abc
from typing import List

from django.core.management import call_command


class AbstractExecutor(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def run(self, command: List[str]) -> None:
        raise NotImplementedError


class DjangoExecutor:
    def run(self, commands):
        call_command(*commands)
