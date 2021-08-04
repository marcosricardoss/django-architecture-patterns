import uuid
from eventprocessor.adapters.broker import RedisBroker

def test_redis_broker_subscribe():
    channel = f"events:{uuid.uuid1().hex}"
    broker = RedisBroker(ignore_subscribe_messages=False)
    broker.subscribe(channel)    
    while True:
        data = broker.pubsub.get_message()
        if data and data["channel"]:
            assert data["channel"]==channel.encode()
            break


def test_redis_broker_listen():
    channel = f"events:{uuid.uuid1().hex}"
    broker = RedisBroker(ignore_subscribe_messages=False)
    broker.subscribe(channel)
    for event in broker.listen():
        if event: 
            assert event["channel"] == channel.encode() 
            assert event["data"] == 1
            break
