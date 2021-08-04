
import logging

from .adapters import broker

logger = logging.getLogger("eventprocessor")

class EventConsumer:
    def __init__(self, broker:broker.AbstractBroker, handlers:dict) -> None:
        self.handlers = handlers
        self.broker = broker
    
    def _subscribe(self):
        for channel in self.handlers:
            self.broker.subscribe(channel)
    
    def _process_event(self, channel, data):
        for handler in self.handlers[channel]:
            try:
                logger.debug(f"handling event '{channel}' with handler '{handler}'")
                handler(data)
            except BaseException as e:  # pragma: no cover
                logger.error(f"Exception handling event '{channel}' with handler {handler}': {e}")                
                continue
    
    def run(self):
        self._subscribe()
        for event in self.broker.listen():                    
            self._process_event(event["channel"].decode(), event["data"].decode())