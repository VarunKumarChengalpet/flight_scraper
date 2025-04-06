import redis
import json

r = redis.Redis(host="localhost", port=6379, db=1)

def get_cached_flight(key: str):
    data = r.get(key)
    return json.loads(data) if data else None

def set_cached_flight(key: str, data: dict, ttl: int = 450):
    r.setex(key, ttl, json.dumps(data))
