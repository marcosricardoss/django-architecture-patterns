import os
import json
import logging

from redis import Redis

logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger("eventconsumer")

config = {
    "host": os.environ.get("REDIS_HOST"),
    "port": int(os.environ.get("REDIS_PORT")),
    "db": 0,
}
r = Redis(**config)


def main():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("task_created_event")
    for m in pubsub.listen():
        send_task_created_notification(m)


def send_task_created_notification(m):
    logger.info(f"handling {m}")
    data = json.loads(m["data"])
    logger.info(f"handling {str(data)}")


if __name__ == "__main__":
    main()
