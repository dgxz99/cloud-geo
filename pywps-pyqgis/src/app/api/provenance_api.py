import flask

from app.dao.mongo import MongoDB
from app.utils.json_response import JsonResponse

# 创建flask蓝图
provenance_blue = flask.Blueprint('provenance', __name__)


@provenance_blue.route('/provenances/job_id/<job_id>', methods=['GET'])
def get_job_provenances(job_id):
	mongo = MongoDB()
	provenance = mongo.get_one("provenance", {"_id": job_id})
	mongo.close()
	if not provenance:
		return JsonResponse.error({"message": "Job not found"})
	return JsonResponse.success(provenance)


@provenance_blue.route('/provenances/identifier/<path:identifier>', methods=['GET'])
def get_identifier_provenances(identifier):
	mongo = MongoDB()
	provenance = mongo.find_many("provenance", {"name": identifier})
	mongo.close()
	if not provenance:
		return JsonResponse.success(data={"count": 0, "data": []})
	return JsonResponse.success(data={
		"count": len(provenance),
		"data": provenance
	})
