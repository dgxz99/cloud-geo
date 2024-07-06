from context.config import get_config
from pymongo import MongoClient, errors
from typing import List, Dict

config = get_config()


class MongoDB:
	def __init__(self):
		host = config.get("MongoDB", "host", fallback="localhost")
		port = config.getint("MongoDB", "port", fallback=27017)
		db_name = config.get("MongoDB", "db_name", fallback=None)
		username = config.get("MongoDB", "username", fallback=None)
		password = config.get("MongoDB", "password", fallback=None)

		self.client = MongoClient(host, port, username=username, password=password)
		self.db = self.client[str(db_name)]

	def add_one(self, collection_name, document: Dict):
		try:
			collection = self.db[collection_name]
			collection.insert_one(document)
		except errors.DuplicateKeyError:
			print(f"算子{document.get('Identifier')}已存在！")

	def add_many(self, collection_name, documents: List[Dict]):
		collection = self.db[collection_name]
		existing_doc = []
		# 查询数据库中已存在的文档，并将其 Identifier 值保存在列表中
		existing_documents = collection.find({"Identifier": {"$in": [doc['Identifier'] for doc in documents]}})
		for doc in existing_documents:
			print(f"算子{doc['Identifier']}已存在！")
			existing_doc.append(doc['Identifier'])

		# 从待插入文档列表中移除已存在的文档
		documents = [doc for doc in documents if doc['Identifier'] not in set(existing_doc)]
		if documents:
			# 批量插入文档
			collection.insert_many(documents)

	def find_one(self, collection_name, query):
		collection = self.db[collection_name]
		return collection.find_one(query)

	def find_many(self, collection_name, query):
		collection = self.db[collection_name]
		return list(collection.find(query))

	def find_all(self, collection_name):
		collection = self.db[collection_name]
		return list(collection.find())

	def update_document(self, collection_name, query, update):
		collection = self.db[collection_name]
		result = collection.update_one(query, {'$set': update})
		return result.modified_count

	def delete_document(self, collection_name, query):
		collection = self.db[collection_name]
		result = collection.delete_one(query)
		return result.deleted_count

	def delete_all_documents(self, collection_name):
		collection = self.db[collection_name]
		result = collection.delete_many({})
		return result.deleted_count

	def close(self):
		self.client.close()
