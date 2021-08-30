import abc
import time
import uuid
import json

from redis import StrictRedis
from eventprocessor.utils import dumphandler
from eventprocessor.settings import REDIS_CONFIG

class AbstractPublisher(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def publish(self, *args, **kwargs):
        raise NotImplementedError

class REDISPublisher(AbstractPublisher):     
    """ Redis Publisher """

    def __init__(self) -> None:
        self.redis = StrictRedis(**REDIS_CONFIG)

    def publish(self, _topic, _action, _entity):
        key = 'events:{{{0}}}_{1}'.format(_topic, _action)        
        entry_id = '{0:.6f}'.format(time.time()).replace('.', '-')                
        result = self.redis.xadd(key, {
            'event_id': str(uuid.uuid4()),
            'entity': json.dumps(_entity, default=dumphandler)
        }, id=entry_id)
        return result