import redis
from config import get_config

config = get_config()


class RedisClient:
	def __init__(self):
		host = config.get("Redis", "host", fallback="localhost")
		port = config.getint("Redis", "port", fallback=6379)
		db = config.getint("Redis", "db", fallback=0)
		password = config.get("Redis", "password", fallback=None)
		self.client = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)

	def set(self, key, value):
		self.client.set(key, value)

	def setex(self, key, time_in_seconds, value):
		self.client.setex(key, time_in_seconds, value)

	def get(self, key):
		return self.client.get(key)

	def delete(self, key):
		self.client.delete(key)

	def exists(self, key):
		return self.client.exists(key)

	def keys(self, pattern='*'):
		return self.client.keys(pattern)

	def hset(self, name, key, value):
		self.client.hset(name, key, value)

	def hget(self, name, key):
		return self.client.hget(name, key)

	def hdel(self, name, key):
		self.client.hdel(name, key)

	def hkeys(self, name):
		return self.client.hkeys(name)

	def hgetall(self, name):
		return self.client.hgetall(name)
