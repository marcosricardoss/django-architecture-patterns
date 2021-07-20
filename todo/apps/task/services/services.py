from typing import Optional, Union
from datetime import datetime

from django.db import IntegrityError, transaction

from ..models import Task
from .unit_of_work import AbstractUnitOfWork
from .exceptions import TaskException
from . import messagebus
from . import events


def add_task_service(
    title: str,
    description: str,
    deadline_at: datetime,
    finished_at: Optional[datetime],
    uow: Union[AbstractUnitOfWork, transaction.Atomic],
):

    """Example of using an Unit of Work in a service layer. We could put code
    here that is not directly linked to a domain model, such as accessing an external API.
    The purpose of a UOW is to guarantee the atomicity and integrity of information in the database."""

    try:
        with uow:
            task = Task()
            task.title = title
            task.description = description
            task.deadline_at = deadline_at
            task.finished_at = finished_at
            task.save()
            messagebus.handle(events.TaskCreated(title, deadline_at))
    except IntegrityError as e:
        raise TaskException(f"Error saving task to database: {e}")
