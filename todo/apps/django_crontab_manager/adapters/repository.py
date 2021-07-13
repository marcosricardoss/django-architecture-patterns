import abc
from typing import List

from django.db.models import Model as DjangoModel


class AbstractRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def get(self, reference) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[object]:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def __init__(self, Model: DjangoModel) -> None:
        self._model = Model

    @property
    def model(self):
        return self._model

    def get(self, id: int) -> DjangoModel:
        return self._model.objects.filter(id=id).first()

    def list(self) -> List[DjangoModel]:
        return self._model.objects.all()

    def delete(self) -> None:
        self._model.objects.all().delete()