import time
import json
from datetime import datetime

from app.dao.RedisClient import RedisClient


class JobStoreStrategy:
	def save_job(self, job_id, job_data):
		raise NotImplementedError

	def get_job(self, job_id):
		raise NotImplementedError

	def cleanup_expired_jobs(self):
		raise NotImplementedError


class InMemoryJobStore(JobStoreStrategy):
	def __init__(self):
		self.job_store = {}

	def save_job(self, job_id, job_data):
		self.job_store[job_id] = job_data

	def save_job_timed(self, job_id, job_data):
		self.job_store[job_id] = job_data

	def get_job(self, job_id):
		return self.job_store.get(job_id)

	def del_job(self, job_id):
		del self.job_store[job_id]

	def cleanup_expired_jobs(self):
		# 获取当前UTC时间
		current_timestamp = time.time()
		expired_jobs = []
		for job_id, job_data in self.job_store.items():
			job_result = json.loads(job_data)['result']
			if job_result is None or job_result['status'] == 'Running':
				continue

			if job_result['status'] == 'failed':
				expired_jobs.append(job_id)
				continue

			# 将ISO 8601格式的字符串转换为datetime对象
			expiration_time = datetime.fromisoformat(job_result['expirationTime'])
			# 将datetime对象转换为时间戳
			expiration_timestamp = expiration_time.timestamp()
			if current_timestamp - expiration_timestamp > 24 * 60 * 60:
				expired_jobs.append(job_id)
		for job_id in expired_jobs:
			del self.job_store[job_id]


class RedisJobStore(JobStoreStrategy):
	def __init__(self):
		# RedisClient对象
		self.redis_client = RedisClient()

	def save_job(self, job_id, job_data):
		self.redis_client.set(job_id, json.dumps(job_data))

	def save_job_timed(self, job_id, job_data):
		self.redis_client.setex(job_id, 24 * 60 * 60, json.dumps(job_data))

	def get_job(self, job_id):
		job_data = self.redis_client.get(job_id)
		return json.loads(job_data) if job_data else None

	def del_job(self, job_id):
		self.redis_client.delete(job_id)

	def cleanup_expired_jobs(self):
		# Redis 会自动处理过期数据，所以这里可以是空实现
		pass
