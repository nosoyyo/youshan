import redis


class Base():
    cpool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=cpool)
