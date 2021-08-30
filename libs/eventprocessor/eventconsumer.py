import json
import logging
import functools

from .adapters.subscriber import AbstractSubscriber
from .adapters.cache import AbstractCache

logger = logging.getLogger("eventprocessor")

class EventConsumer:
    def __init__(self, _subscriber:AbstractSubscriber, _cache: AbstractCache) -> None: 
        self.subscriber = _subscriber
        self.subscribers = {}
        self.cache = _cache

    def _entity_created(self, _topic, _item):
        """
        Event handler for entity created events, i.e. create a cached entity.

        :param _topic: The entity type.
        :param _item: A dict with entity properties.
        """        
        
        if self.cache.exists(_topic):            
            entity = json.loads(_item['entity'])
            self.cache.create(_topic, entity)

    def _entity_deleted(self, _topic, _item):
        """
        Event handler for entity deleted events, i.e. delete a cached entity.

        :param _topic: The entity type.
        :param _item: A dict with entity properties.
        """
        if self.cache.exists(_topic):
            entity = json.loads(_item['entity'])
            self.cache.delete(_topic, entity)

    def _entity_updated(self, _topic, _item):
        """
        Event handler for entity updated events, i.e. update a cached entity.

        :param _topic: The entity type.
        :param _item: A dict with entity properties.
        """
        if self.cache.exists(_topic):
            entity = json.loads(_item['entity'])
            self.cache.update(_topic, entity)

    def subscribe(self, _topic, _action, _handler):
        """
        Subscribe to an event channel.

        :param _topic: The event topic.
        :param _action: The event action.
        :param _handler: The event handler.
        :return: Success.
        """
        if (_topic, _action) in self.subscribers:
            self.subscribers[(_topic, _action)].add_handler(_handler)
        else:
            subscriber = self.subscriber.create(_topic, _action, _handler)
            subscriber.start()
            self.subscribers[(_topic, _action)] = subscriber

    def unsubscribe(self, _topic, _action, _handler):
        """
        Unsubscribe from an event channel.

        :param _topic: The event topic.
        :param _action: The event action.
        :param _handler: The event handler.
        :return: Success.
        """
        subscriber = self.subscribers.get((_topic, _action))
        if not subscriber:
            return False

        subscriber.remove_handler(_handler)
        if not subscriber:
            subscriber.stop()
            del self.subscribers[(_topic, _action)]    


    def activate_entity_cache(self, _topic):
        """
        Keep entity cache up to date.

        :param _topic: The entity type.
        """
        self.subscribe(_topic, 'created', functools.partial(self._entity_created, _topic))
        self.subscribe(_topic, 'deleted', functools.partial(self._entity_deleted, _topic))
        self.subscribe(_topic, 'updated', functools.partial(self._entity_updated, _topic))


    def deactivate_entity_cache(self, _topic):
        """
        Stop keeping entity cache up to date.

        :param _topic: The entity type.
        """
        self.unsubscribe(_topic, 'created', functools.partial(self._entity_created, _topic))
        self.unsubscribe(_topic, 'deleted', functools.partial(self._entity_deleted, _topic))
        self.unsubscribe(_topic, 'updated', functools.partial(self._entity_updated, _topic))