import pymongo as pym
from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['apirestfulencincominutos']
alertas = db.alertas

alertasPorBarrioMes = []

def llenarListaJson(pConjunto):
    cursor = alertas.find({})
    for document in cursor:
        if(document['Conjunto'] == pConjunto ):
            alertasPorBarrioMes.append(document)
        
llenarListaJson('Mirandela')
print(alertasPorBarrioMes)
