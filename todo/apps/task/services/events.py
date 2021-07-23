from dataclasses import dataclass
from datetime import datetime


class Event:
    pass


@dataclass
class TaskCreated(Event):
    title: str    
    deadline_at: datetime

@dataclass
class TaskUpdated(Event):
    title: str    
    deadline_at: datetime
    updated_at: datetime