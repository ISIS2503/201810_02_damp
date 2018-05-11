import pymongo as pym

from pym import MongoClient
client = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.Alertas

cursor = collection.find({'Correo': (correo)})
        for document in cursor:
            rol = document['Rol']
