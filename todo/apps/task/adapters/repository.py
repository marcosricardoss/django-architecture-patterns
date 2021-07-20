import abc
from typing import List

from django.db import IntegrityError
from django.db.models import Model as DjangoModel

from task.exceptions import ObjectDoesNotExist, CreateObjectException, UpdateObjectException

class AbstractRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def create(data, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id, *args, **kwargs) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id, data, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> List[object]:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def __init__(self, Model: DjangoModel) -> None:
        self._model = Model

    @property
    def model(self):
        return self._model

    def create(self, data, *args, **kwargs):
        try: 
            return self._model.objects.create(**data)
        except IntegrityError:
            raise CreateObjectException(f"Error creating object")        

    def get(self, id: int, *args, **kwargs) -> DjangoModel:
        try:
            return self._model.objects.get(id=id)
        except self._model.DoesNotExist:
            raise ObjectDoesNotExist(f"Error trying to retrieve object with id={id}")

    def update(self, id, data, *args, **kwargs):
        try:
            obj = self.get(id)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        except BaseException:
            raise UpdateObjectException(f"Error updating object with id={id}")
        

    def delete(self, id, *args, **kwargs) -> None:
        return self._model.objects.filter(id=id).delete()

    def list(self, *args, **kwargs) -> List[DjangoModel]:
        return self._model.objects.all()
