import logging

from .adapters import publisher

logger = logging.getLogger("django")

class EventPublisher:        
    def __init__(self, publisher:publisher.AbstractPublisher) -> None:   
        self.publisher = publisher

    def publish(self, _topic, _action, _entity) -> None:
        logging.debug(f"publishing: _topic={_topic}, _action={_action}, data={_entity}", )
        self.publisher.publish(_topic, _action, _entity)
