import logging

from redis import Redis
from django.conf import settings

logger = logging.getLogger("eventprocessor")

# redis conection
config = getattr(settings, "REDIS_CONFIG")
r = Redis(**config)

class EventConsumer:
    def __init__(self, handlers:dict) -> None:
        self._handlers = handlers
        self._pubsub = r.pubsub(ignore_subscribe_messages=True)            
    
    def _subscribe(self):
        for channel in self._handlers:
            self._pubsub.subscribe(channel)
    
    def _process_event(self, channel, data):
        for handler in self._handlers[channel]:
            try:
                logger.debug(f"handling event '{channel}' with handler '{handler}'")
                handler(data)
            except BaseException as e:  # pragma: no cover
                logger.error(f"Exception handling event '{channel}' with handler {handler}': {e}")                
                continue
    
    def run(self):
        self._subscribe()
        for event in self._pubsub.listen():                    
            self._process_event(event["channel"].decode(), event["data"].decode())