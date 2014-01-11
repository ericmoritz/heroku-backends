import os
import redis
from collections import namedtuple

def redis_client():
    return _client


###-------------------------------------------------------------------
### Internal
###-------------------------------------------------------------------
RedisConfig = namedtuple("RedisConfig", ["host", "port", "db", "password"])
def _redis_url():
    try:
        preferred_keys = [os.environ["REDIS_BACKEND"]]
    except:
        preferred_keys = []


    for key in preferred_keys + ["OPENREDIS_URL", "REDISTOGO_URL"]:
        if key in os.environ:
            return os.environ[key]
    return "redis://localhost"


def _redis_config(db=None):
    from redis.client import urlparse

    url = _redis_url()
    url = urlparse(url)
    
    # We only support redis:// schemes.
    assert url.scheme == 'redis' or not url.scheme

    # Extract the database ID from the path component if hasn't been given.
    if db is None:
        try:
            db = int(url.path.replace('/', ''))
        except (AttributeError, ValueError):
            db = 0
            
    host = url.hostname
    port = int(url.port or 6379)

    return RedisConfig(host, port, db, url.password)

_conf = _redis_config()
_client = redis.StrictRedis(host=_conf.host, port=_conf.port, db=_conf.db, password=_conf.password)

