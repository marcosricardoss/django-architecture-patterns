import os
import logging
# using django app context
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django;django.setup()

from .handlers import send_task_notification
from eventprocessor import EventConsumer, REDISSubscriber, REDISCache


logger = logging.getLogger("eventprocessor")

if __name__ == "__main__":                
    try:        
        consumer = EventConsumer(REDISSubscriber, REDISCache())
        consumer.activate_entity_cache("task")
        consumer.subscribe("task", "created", send_task_notification)
    except KeyboardInterrupt: 
        logger.info("exiting...")
