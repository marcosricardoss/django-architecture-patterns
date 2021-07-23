from typing import Optional, Union
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from task.adapters import AbstractRepository
from .unit_of_work import AbstractUnitOfWork
from . import messagebus
from . import events


def add_task_service(
    title: str,
    description: str,
    deadline_at: datetime,
    finished_at: Optional[datetime],
    repository: AbstractRepository,
    uow: Union[AbstractUnitOfWork, transaction.Atomic],
):

    """Example of using an Unit of Work in a service layer. We could put code
    here that is not directly linked to a domain model, such as accessing an external API.
    The purpose of a UOW is to guarantee the atomicity and integrity of information in the database."""

    defaults = {
        "title": title,
        "description": description,
        "deadline_at": deadline_at,
        "finished_at": finished_at
    }
    with uow:
        repository.create(
            data = defaults
        )
        messagebus.handle(events.TaskCreated(title, deadline_at))
    

def update_task_service(
    id: int,
    title: str,
    description: str,
    deadline_at: datetime,
    finished_at: Optional[datetime],
    repository: AbstractRepository,
    uow: Union[AbstractUnitOfWork, transaction.Atomic],
):

    """Example of using an Unit of Work in a service layer. We could put code
    here that is not directly linked to a domain model, such as accessing an external API.
    The purpose of a UOW is to guarantee the atomicity and integrity of information in the database."""

    defaults = {
        "title": title,
        "description": description,
        "deadline_at": deadline_at,
        "finished_at": finished_at
    }
    with uow:
        obj = repository.update(
            id = id,
            data = defaults
        )
        messagebus.handle(events.TaskUpdated(title, deadline_at, obj.updated_at))


def detele_task_service(
    id: int,    
    repository: AbstractRepository,
    uow: Union[AbstractUnitOfWork, transaction.Atomic],
):

    """Example of using an Unit of Work in a service layer. We could put code
    here that is not directly linked to a domain model, such as accessing an external API.
    The purpose of a UOW is to guarantee the atomicity and integrity of information in the database."""
    
    with uow:
        repository.delete(id)
        messagebus.handle(events.TaskDeleted(id=id, deleted_at=timezone.now()))
            
    