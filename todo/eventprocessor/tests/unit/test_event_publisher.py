from eventprocessor import EventPublisher

from .fakebroker import FakeBroker, FAKE_CHANNEL, FAKE_DATA

def test_event_consumer():    
    broker = FakeBroker()
    ep = EventPublisher(broker=broker)
    ep.publish(FAKE_CHANNEL, FAKE_DATA)    
    assert (FAKE_CHANNEL,FAKE_DATA) in broker._published_data    

    