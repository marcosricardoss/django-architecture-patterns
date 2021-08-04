import logging
from typing import List, Dict, Callable, Type

from .handlers import send_task_notification
from .topics import Topic
from .actions import Action
from .eventconsumer import EventConsumer
from .adapters.broker import RedisBroker
from .utils import get_channel_name

logger = logging.getLogger("eventprocessor")

HANDLERS = {
    get_channel_name(Topic.TASK, Action.CREATED): [send_task_notification],
    get_channel_name(Topic.TASK, Action.UPDATED): [send_task_notification],
    get_channel_name(Topic.TASK, Action.DELETED): [send_task_notification],    
}  # type: Dict[Type[str], List[Callable]]

if __name__ == "__main__":                
    try:
        EventConsumer(broker=RedisBroker(), handlers=HANDLERS).run()
    except KeyboardInterrupt: 
        logger.info("exiting...")
