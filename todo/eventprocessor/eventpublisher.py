import logging
from redis import Redis
from django.conf import settings

logger = logging.getLogger("django")

config = getattr(settings, "REDIS_CONFIG")
r = Redis(**config)

class EventPublisher:
    def publish(self, channel, data):
        logging.debug(f"publishing: channel={channel}, event={data}")
        r.publish(channel, data)
