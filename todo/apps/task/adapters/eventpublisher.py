import json
import logging
from dataclasses import asdict
from datetime import datetime
from redis import Redis

from django.conf import settings

from task.services import events

logger = logging.getLogger("django")

config = getattr(settings, "REDIS_CONFIG")
r = Redis(**config)


def dump_handler(x): # pragma: no cover
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def publish(channel, event: events.Event):
    logging.debug("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event), default=dump_handler))
