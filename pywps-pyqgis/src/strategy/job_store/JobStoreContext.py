from .JobStoreStrategy import InMemoryJobStore, RedisJobStore


class JobStoreContext:
	def __init__(self, deploy_mode):
		self.deploy_mode = deploy_mode

	def job_store_strategy(self):
		if self.deploy_mode == 'single':
			job_store_strategy = InMemoryJobStore()
		elif self.deploy_mode == 'distributed':
			job_store_strategy = RedisJobStore()
		else:
			raise ValueError("Invalid deployment mode!")

		return job_store_strategy
