import uuid
from datetime import datetime

def dumphandler(x):  # pragma: no cover
    if isinstance(x, datetime):
        return x.isoformat()
    if isinstance(x, uuid.UUID):
        return str(x)
    raise TypeError("Unknown type")    