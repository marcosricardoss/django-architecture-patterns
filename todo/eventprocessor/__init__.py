import os
import logging

# using django app context
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django;django.setup()

# logging settings
logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger("eventprocessor")

from .eventconsumer import EventConsumer
from .eventpublisher import EventPublisher