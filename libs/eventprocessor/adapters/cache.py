import abc
import json

from redis import StrictRedis
from eventprocessor.settings import REDIS_CONFIG

def is_key(_value):
    """
    Check if a value is a key, i.e. has to be looked up on Redis root level.

    :param _value: The string to be checked.
    :return: True if the given value is a Redis key, false otherwise.
    """
    return '_' in _value and ':' in _value


class AbstractCache(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def find_one(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, *args, **kwargs):
        raise NotImplementedError


class REDISCache(AbstractCache):
    """
    Redis Cache class.
    """
    redis = None

    def __init__(self):
        """
        :param _redis: A redis instance.
        """
        self.redis = StrictRedis(**REDIS_CONFIG)

    def create(self, _topic, _values):
        """
        Set an entity.

        :param _topic: The type of entity.
        :param _values: The entity properties.
        """
        self.redis.sadd('{}_ids'.format(_topic), _values['id'])
        for k, v in _values.items():
            if isinstance(v, list):
                lid = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, lid)
                self.redis.rpush(lid, *v)
            elif isinstance(v, set):
                sid = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, sid)
                self.redis.sadd(sid, *v)
            elif isinstance(v, dict):
                did = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, did)
                self.redis.hmset(did, v)
            else:
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, v)

    def retrieve(self, _topic):
        """
        Get an entity.

        :param _topic: The type of entity.
        :return: A dict with the entity properties.
        """
        result = {}
        for eid in self.redis.smembers('{}_ids'.format(_topic)):
            result[eid] = self.redis.hgetall('{}_entity:{}'.format(_topic, eid))
            for k, v in result[eid].items():
                if is_key(v):
                    rtype = self.redis.type(v)
                    if rtype == 'list':
                        result[eid][k] = self.redis.lrange(v, 0, -1)
                    elif rtype == 'set':
                        result[eid][k] = self.redis.smembers(v)
                    elif rtype == 'hash':
                        result[eid][k] = self.redis.hgetall(v)
                    else:
                        raise ValueError('unknown redis type: {}'.format(rtype))
        return result

    def update(self, _topic, _values):
        """
        Delete and set an entity.

        :param _topic: The type of entity.
        :param _values: The entity properties.
        """
        for k, v in _values.items():
            if isinstance(v, list):
                lid = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, lid)
                self.redis.delete(lid)
                self.redis.rpush(lid, *v)
            elif isinstance(v, set):
                sid = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, sid)
                self.redis.delete(sid)
                self.redis.sadd(sid, *v)
            elif isinstance(v, dict):
                did = '{}_{}:{}'.format(_topic, k, _values['id'])
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, did)
                self.redis.delete(did)
                self.redis.hmset(did, *v)
            else:
                self.redis.hset('{}_entity:{}'.format(_topic, _values['id']), k, v)

    def delete(self, _topic, _values):
        """
        Delete an entity.

        :param _topic: The type of entity.
        :param _values: The entity properties.
        """
        self.redis.srem('{}_ids'.format(_topic), 1, _values['id'])
        self.redis.delete('{}_entity:{}'.format(_topic, _values['id']))
        for k, v in _values.items():
            if isinstance(v, (list, set, dict)):
                self.redis.delete('{}_{}:{}'.format(_topic, k, _values['id']))

    def exists(self, _topic):
        """
        Check if an entity exists.

        :param _topic: The type of entity.
        :return: True iff an entity exists, else False.
        """
        return self.redis.exists('{}_ids'.format(_topic))

    
    def find_one(self, _topic, _id):
        """
        Find an entity for a topic with an specific id.

        :param _topic: The event topic, i.e. name of entity.
        :param _id: The entity id.
        :return: A dict with the entity.
        """
        return self.find_all(_topic).get(_id)
    
    
    def find_all(self, _topic):
        """
        Find all entites for a topic.

        :param _topic: The event topic, i.e name of entity.
        :return: A dict mapping id -> entity.
        """
        def _get_entities(_events):
            entities = map(lambda x: json.loads(x[1]['entity']), _events)
            return dict(map(lambda x: (x['id'], x), entities))

        def _remove_deleted(_created, _deleted):
            for d in _deleted.keys():
                del _created[d]
            return _created

        def _set_updated(_created, _updated):
            for k, v in _updated.items():
                _created[k] = v
            return _created

        # read from cache
        if self.exists(_topic):
            return self.retrieve(_topic)

        # result is a dict mapping id -> entity
        result = {}

        # read all events at once
        with self.redis.pipeline() as pipe:
            pipe.multi()
            pipe.xrange('events:{{{0}}}_created'.format(_topic))
            pipe.xrange('events:{{{0}}}_deleted'.format(_topic))
            pipe.xrange('events:{{{0}}}_updated'.format(_topic))
            created_events, deleted_events, updated_events = pipe.execute()

        # get created entities
        if created_events:
            result = _get_entities(created_events)

        # remove deleted entities
        if deleted_events:
            result = _remove_deleted(result, _get_entities(deleted_events))

        # set updated entities
        if updated_events:
            result = _set_updated(result, _get_entities(updated_events))

        # write into cache
        for value in result.values():
            self.create(_topic, value)

        return result