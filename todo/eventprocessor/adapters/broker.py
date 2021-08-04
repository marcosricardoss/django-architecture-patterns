import abc
import logging

from redis import Redis
from django.conf import settings

logger = logging.getLogger("eventprocessor")

class AbstractBroker(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def subscribe(self, channel, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def listen(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def publish(self, *args, **kwargs):
        raise NotImplementedError


class RedisBroker(AbstractBroker):
    def __init__(self, ignore_subscribe_messages=True) -> None:        
        config = getattr(settings, "REDIS_CONFIG")
        self.broker = Redis(**config)
        self.pubsub = self.broker.pubsub(ignore_subscribe_messages=ignore_subscribe_messages)            
    
    def subscribe(self, channel):    
        self.pubsub.subscribe(channel)
    
    def listen(self):        
        return self.pubsub.listen()
    
    def publish(self, channel, data):
        self.broker.publish(channel, data)
