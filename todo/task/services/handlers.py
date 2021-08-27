from task.adapters import email
from . import events

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


def send_task_deleted_notification(event: events.TaskDeleted):
    email.send_mail(
        "manager@email.com",
        f"The task with ID {event.id} was deleted at {event.deleted_at}",
    )