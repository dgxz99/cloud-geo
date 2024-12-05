import json
import time
import requests
import threading


def run_job(job_store_strategy, data, job_id):
	"""
	运行job任务
	Args:
		job_store_strategy: 存储job任务的策略
		data: 请求体
		job_id: job-id
	"""
	response = None
	try:
		data['job_id'] = job_id
		response = requests.post('http://127.0.0.1:5000/jobs', json=data, timeout=36000).json()
		job_data = {
			"jobId": job_id,
			"status": response['data']['status'],
			"result": response['data'],
			"timestamp": time.time()
		}
	except:
		job_data = {
			"jobId": job_id,
			"status": "failed",
			"result": None,
			"timestamp": time.time()
		}

	# 将任务状态和结果存储起来
	job_store_strategy.save_job_timed(job_id, json.dumps(job_data))
	return response


def cleanup_thread_func(job_store_strategy):
	while True:
		job_store_strategy.cleanup_expired_jobs()
		time.sleep(3600)  # 每小时检查一次


def start_cleanup_thread(job_store_strategy):
	cleanup_thread = threading.Thread(target=cleanup_thread_func, args=(job_store_strategy,), daemon=True)
	cleanup_thread.start()
