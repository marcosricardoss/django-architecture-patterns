from typing import List, Dict, Callable, Type

from task.adapters import email
from . import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_task_created_notification(event: events.TaskCreated):
    email.send_mail(
        "manager@email.com",
        f"The task '{event.title}' was created with deadline at {event.deadline_at}",
    )

def send_task_updated_notification(event: events.TaskUpdated):
    email.send_mail(
        "manager@email.com",
        f"The task '{event.title}' created with deadline at {event.deadline_at} was updated at {event.updated_at}",
    )

HANDLERS = {
    events.TaskCreated: [send_task_created_notification],
    events.TaskUpdated: [send_task_updated_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
