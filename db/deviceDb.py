from fileinput import filename
import json
import pymongo
from bson import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb://ammar:dmk123@192.168.0.8:27017/?authMechanism=DEFAULT")
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
    update_doc = {'$set': {'timestamp': ts}}
    if existing_doc:
        if sensors:
            for key in sensors:
                update_doc['$set'][f'sensors.{key}'] = sensors[key]
        if actuators:
            for key in actuators:
                update_doc['$set'][f'actuators.{key}'] = actuators[key]
        collection.update_one({'chipID': id}, update_doc)
    else:
        # Otherwise, create a new document with the specified chipID and data
        new_doc = {'chipID': id, 'timestamp': ts}
        if sensors:
            new_doc = {'chipID': id, 'timestamp': ts, 'sensors': sensors}
        if actuators:
            new_doc= {'chipID': id, 'timestamp': ts, 'actuators': actuators} 
        collection.insert_one(new_doc)

def insertOtaBins(vClass,vName,vNumber, fileName):
    collection = db['ota']
    dt= datetime.now()
    ts = datetime.timestamp(dt)
    new_doc = {'vClass': vClass, 'vName': vName, 'vNumber': vNumber, 'timestamp': ts, 'fileName': fileName}
    collection.insert_one(new_doc)
    
def getOta(vClass=None):
    collection = db['ota']
    if vClass:
        documents= collection.find_one({"vClass": vClass}, sort=[("timestamp", pymongo.DESCENDING)])
    else: 
        documents= list(collection.find(sort=[("timestamp", pymongo.DESCENDING)]))
    return json.dumps(documents, cls=CustomJSONEncoder)


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