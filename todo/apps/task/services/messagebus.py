from typing import List, Dict, Callable, Type

from task.adapters import email
from . import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_task_created_notification(event: events.TaskCreated):
    email.send_mail(
        "manager@email.com",
        f"task '{event.title}' create with deadline at {event.deadline_at}",
    )


HANDLERS = {
    events.TaskCreated: [send_task_created_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
