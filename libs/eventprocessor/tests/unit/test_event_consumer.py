from eventprocessor import EventConsumer

from .fakebroker import FakeBroker, FAKE_CHANNEL, FAKE_DATA

def test_event_consumer():    
    fakebroker = FakeBroker()
    handlers = { FAKE_CHANNEL: [fakebroker.handler] } 

    ec = EventConsumer(broker=fakebroker, handlers=handlers)
    ec.run()
    assert FAKE_CHANNEL in fakebroker._subscribed_channels
    assert FAKE_DATA in fakebroker._data_handler
    assert fakebroker._listen

    