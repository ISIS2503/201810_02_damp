import pymongo as pym
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['apirestfulencincominutos']
alertas = db.alertas

print(alertas.find_one({'_id': ObjectId("5af4f5304e7b7d312ca09199")}))


