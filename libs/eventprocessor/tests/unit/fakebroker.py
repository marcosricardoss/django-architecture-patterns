from eventprocessor import AbstractBroker

FAKE_CHANNEL = "FAKE_CHANNEL"
FAKE_DATA = "{'a':1,'b':1}"

class FakeBroker(AbstractBroker):
    def __init__(self) -> None:        
        self._listen = False
        self._published_data = list()
        self._subscribed_channels = list()
        self._data_handler = list()
        self._listen_iterable = [
            {
                "channel": FAKE_CHANNEL.encode(),
                "data": FAKE_DATA.encode()
            }
        ]
    
    def subscribe(self, channel):    
        self._subscribed_channels.append(channel)
    
    def listen(self):        
        self._listen = True
        return self._listen_iterable
    
    def publish(self, channel, data):
        self._published_data.append((channel, data))

    def handler(self, data):
        self._data_handler.append(data)