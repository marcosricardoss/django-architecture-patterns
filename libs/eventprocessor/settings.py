import os 

REDIS_CONFIG = {
    "db": 0,
    "decode_responses": True,
    "host": os.environ.get("REDIS_HOST"),
    "port": int(os.environ.get("REDIS_PORT")),
}