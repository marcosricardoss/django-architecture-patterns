from adapters.cache import AbstractCache

class Cacher:

    def __init__(self, cache:AbstractCache) -> None:
        self.cache = cache

    def find_one(self, _topic, _id):
        """
        Find an entity for a topic with an specific id.

        :param _topic: The event topic, i.e. name of entity.
        :param _id: The entity id.
        :return: A dict with the entity.
        """
        return self.cache(_topic).get(_id)

    def find_all(self, _topic):
        """
        Find all entites for a topic.

        :param _topic: The event topic, i.e name of entity.
        :return: A list with all entitys.
        """
        return list(self.cache(_topic).values())