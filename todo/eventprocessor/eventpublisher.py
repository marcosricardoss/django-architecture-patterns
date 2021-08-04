import logging

from .adapters import broker

logger = logging.getLogger("django")

class EventPublisher:        
    def __init__(self, broker:broker.AbstractBroker) -> None:   
        self.broker = broker

    def publish(self, channel, data):
        logging.debug(f"publishing: channel={channel}, event={data}")
        self.broker.publish(channel, data)
