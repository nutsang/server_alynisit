from pymongo import MongoClient
import random

class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database_name="database_alynisit", collection_name="hardware"):
        try:
            self._connection = MongoClient(username="TGR_GROUP3", password="ZK984B", host=host, port=port, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id

print('[*] Pushing data to MongoDB ')
mongo_db = MongoDB()

data_list = list()
for data_fake in range(1,6):
    data_list.append({'water_level': round(random.uniform(108, 119), 1)})

for collection in data_list:
    print('[!] Inserting - ', collection)
    mongo_db.insert(collection)