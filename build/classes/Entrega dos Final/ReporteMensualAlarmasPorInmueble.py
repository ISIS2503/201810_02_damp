import pymongo as pym
from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['apirestfulencincominutos']
alertas = db.alertas

alertasPorBarrioMes = []

def llenarListaJson(pMes, pConjunto,pTorre,pPiso,pApartamento):
    cursor = alertas.find({})
    for document in cursor:
        hourT = document['Hora']
        mes = hourT.month
        if(document['Conjunto'] == pConjunto and document['Torre'] == str(pTorre) and document['Piso'] == str(pPiso) and document['Apartamento'] == str(pApartamento) and mes == pMes):
            alertasPorBarrioMes.append(document)
        
llenarListaJson(5,'Mirandela',1,1,1)
print(alertasPorBarrioMes)
