import abc
import logging
import threading

from redis import StrictRedis
from django.conf import settings

rediscfg = getattr(settings, "REDIS_CONFIG")
logger = logging.getLogger("eventprocessor")


class AbstractSubscriber(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def subscribe(self, channel, *args, **kwargs):
        raise NotImplementedError


class REDISSubscriber(threading.Thread):
    """ Redis Subscriber """

    def __init__(self, _topic, _action, _handler, _lastid="$") -> None:
        super(REDISSubscriber, self).__init__()
        self._running = False
        self.handlers = [_handler]
        self.key = "events:{{{0}}}_{1}".format(_topic, _action)
        self.lastid = _lastid
        self.subscribed = True
        self.redis = StrictRedis(**rediscfg)

    def __len__(self):
        return len(self.handlers)

    def _read_stream(self):
        streams = {self.key: self.lastid}
        for streamname, events in self.redis.xread(streams, block=1000):
            for eventID, event in events:
                yield event
                self.lastid = eventID

    def add_handler(self, _handler):
        """
        Add an event handler.

        :param _handler: The event handler function.
        """
        self.handlers.append(_handler)

    def remove_handler(self, _handler):
        """
        Remove an event handler.

        :param _handler: The event handler function.
        """
        self.handlers.remove(_handler)

    def run(self):
        if self._running:
            return

        self._running = True
        while self.subscribed:
            for item in self._read_stream():
                for handler in self.handlers:
                    handler(item)
        self._running = False

    def stop(self):
        """
        Stop polling the event stream.
        """
        self.subscribed = False

    @classmethod
    def create(cls, _topic, _action, _handler, _lastid="$"):
        return cls(_topic, _action, _handler, _lastid)
