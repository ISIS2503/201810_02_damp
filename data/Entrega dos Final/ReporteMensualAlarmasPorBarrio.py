import pymongo as pym
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['apirestfulencincominutos']
alertas = db.alertas

print(alertas.find_one({'_id': ObjectId("5af4f5304e7b7d312ca09199")}))



# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    # Convert from string to ObjectId:
    document = client.db.collection.find_one({'_id': ObjectId(post_id)})


#cursor = collection.find({'Correo': (correo)})
#        for document in cursor:
#            rol = document['Rol']
