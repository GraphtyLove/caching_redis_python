import os
import sys
import redis
import json
from datetime import timedelta


class Cache:
	def __init__(self):
		"""Establish connection with Redis."""
		try:
			print("HOST: ", os.environ.get("REDIS_HOST", "localhost"))
			client = redis.Redis(
				host=os.environ.get("REDIS_HOST", "localhost"),
				port=os.environ.get("REDIS_PORT", 6379),
				db=os.environ.get("REDIS_DB", 0),
			)
			# Verify that Redis is responding
			ping = client.ping()
			if ping is True:
				self.client = client
			else:
				print("Connection established but Redis not responding to ping!")
		# Log error and stop the process if not responding
		except redis.ConnectionError as ex:
			print("Redis Connection Error: ", ex)
			sys.exit(1)

	def get_data_from_cache(self, key: str) -> dict | None:
		"""
		Get data from redis.

		:param key: the key used to store the data in Redis.
		:return data: A dictionary with the data cached if found, None if nothing found with the key.
		"""

		data = self.client.get(key)
		if data is not None:
			data = data.decode("UTF-8")
			data_dict = json.loads(data)
			print("Data fetched from cache")
			data_dict["cache"] = True
			return data_dict
		return None

	def save_data_to_cache(self, key: str, value: dict, exp_in_hours: int = 24) -> bool:
		"""
		Save data to redis.

		:param key: the key used to store the data in Redis.
		:param value: the value associated to the key to save in Redis.
		:param exp_in_hours: The number of hours before expiration of the cached data in Redis.
		:return state: True if the data is well saved in Redis, False if not.
		"""
		str_value = json.dumps(value)
		state = self.client.setex(
			key,
			timedelta(hours=exp_in_hours),
			value=str_value,
		)
		return state
