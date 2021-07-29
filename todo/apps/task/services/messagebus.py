import logging


import logging
from typing import List, Dict, Callable, Type

from . import events
from . import handlers

logger = logging.getLogger("django")


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        try:
            logger.debug(f"handling event {event} with handler {handler}")
            handler(event)
        except BaseException:  # pragma: no cover
            logger.error(f"Exception handling event {event} with handler {handler}")
            continue

HANDLERS = {
    events.TaskCreated: [handlers.send_task_created_notification],
    events.TaskUpdated: [handlers.send_task_updated_notification],
    events.TaskDeleted: [handlers.send_task_deleted_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
