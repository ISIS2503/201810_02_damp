import pymongo as pym
from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['apirestfulencincominutos']
alertas = db.alertas

alertasPorBarrioMes = []

def llenarListaJson(pMes,pConjunto):
    cursor = alertas.find({})
    for document in cursor:
        hourT = document['Hora']
        mes = hourT.month
        if(document['Conjunto'] == pConjunto and mes == pMes):
            alertasPorBarrioMes.append(document)
        
llenarListaJson(3,'Mirandela')

print(alertasPorBarrioMes)
