import logging

from .handlers import send_task_notification
from .eventconsumer import EventConsumer
from .adapters.subscriber import REDISSubscriber
from .adapters.cache import REDISCache

logger = logging.getLogger("eventprocessor")

if __name__ == "__main__":                
    try:        
        consumer = EventConsumer(REDISSubscriber, REDISCache())
        consumer.activate_entity_cache("task")
        consumer.subscribe("task", "created", send_task_notification)
    except KeyboardInterrupt: 
        logger.info("exiting...")
