import abc
from typing import List, Optional

from django.db.models import Model as DjangoModel


class AbstractRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def get(self, reference) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, offset: int, limit: int) -> List[object]:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def __init__(self, Model: DjangoModel) -> None:
        self._model = Model

    @property
    def model(self):
        return self._model

    def get(self, id: int) -> DjangoModel:
        return self._model.objects.filter(id=id).first()

    def list(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> List[DjangoModel]:
        return self._model.objects.all()
