from config import get_config
from pymongo import MongoClient, errors
from typing import List, Dict
from datetime import datetime, timedelta, timezone

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
        self.lock_timeout = 60  # 锁的超时时间（秒）

    # 加锁函数
    def acquire_lock(self, lock_name: str) -> bool:
        """尝试获取分布式锁"""
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.lock_timeout)
        lock = self.db.locks.find_one_and_update(
            {"_id": lock_name, "expires_at": {"$lt": datetime.now(timezone.utc)}},  # 检查是否存在过期锁
            {"$set": {"expires_at": expires_at}},  # 设置新的锁过期时间
            upsert=True,  # 如果锁不存在则插入新记录
            return_document=True
        )
        return lock is not None  # 返回是否成功获取锁

    # 解锁函数
    def release_lock(self, lock_name: str):
        """释放分布式锁"""
        self.db.locks.delete_one({"_id": lock_name})

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
            existing_doc.append(doc['Identifier'])

        # 从待插入文档列表中移除已存在的文档
        documents = [doc for doc in documents if doc['Identifier'] not in set(existing_doc)]
        print(f"The new algorithm_list in the {collection_name} is: {[doc['Identifier'] for doc in documents]}")
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
