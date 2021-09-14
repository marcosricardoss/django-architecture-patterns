import os
import logging

from eventprocessor import EventConsumer, REDISSubscriber, REDISCache
from .handlers import task_created_handler
from app import create_app

logger = logging.getLogger("apieventconsumer")

if __name__ == "__main__":                
    try:        
        app = create_app()
        consumer = EventConsumer(REDISSubscriber, REDISCache())
        consumer.activate_entity_cache("task")
        consumer.subscribe("task", "created", task_created_handler)
    except KeyboardInterrupt: 
        logger.info("exiting...")
