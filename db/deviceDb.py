import json
import pymongo
from bson import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb://ammar:dmk123@server.home:27017/?authMechanism=DEFAULT")
db = client["device"]

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def update_or_insert_doc(collectionName,id, sensors=None, actuators=None):
    dt= datetime.now()
    ts = datetime.timestamp(dt)
    collection = db[collectionName]
    existing_doc = collection.find_one({'chipID': id})
    if existing_doc:
        if sensors:
            collection.update_one({'chipID': id}, {'$set': {'timestamp': ts,'sensors': sensors}})
        if actuators:
            collection.update_one({'chipID': id}, {'$set': {'timestamp': ts,'actuators': actuators}})
    else:
        # Otherwise, create a new document with the specified chipID and data
        if sensors:
            new_doc = {'chipID': id, 'timestamp': ts, 'sensors': sensors}
        if actuators:
            new_doc= {'chipID': id, 'timestamp': ts, 'actuators': actuators} 
        collection.insert_one(new_doc)

def list_all_documents(collection_name,id=None):
    collection = db[collection_name]
    if id:
        print(id)
        documents = collection.find_one({'chipID': id})
    else:
        documents = list(collection.find())
    return json.dumps(documents, cls=CustomJSONEncoder)

def get_all_collections():
    collection_names = db.list_collection_names()
    return json.dumps(collection_names)