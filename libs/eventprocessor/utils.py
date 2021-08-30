from datetime import datetime

def dumphandler(x):  # pragma: no cover
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")    