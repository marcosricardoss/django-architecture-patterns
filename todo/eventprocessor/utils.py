from .topics import Topic
from .actions import Action

def get_channel_name(topic:Topic, action:Action):
    return f"events:{topic.value}_{action.value}"