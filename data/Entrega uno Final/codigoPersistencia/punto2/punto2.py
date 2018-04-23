from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.alertas

class HelloWorld(Resource):
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            x['Alerta' + str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'Activo':v[0], 'Tipo':v[1], 'Conjunto': v[2], 'Torre': v[3], 'Piso': v[4], 'Apartamento': v[5], 'Hora': v[6]}} for k,v in x.items()])
        return thejson

    @app.route("/admin/<name>")
    def getAdmin(name):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            if arreglo[2] == (name) :
               thejson = json.dumps([{ 'Activo':arreglo[0], 'Tipo':arreglo[1], 'Conjunto': arreglo[2], 'Torre': arreglo[3], 'Piso': arreglo[4], 'Apartamento': arreglo[5], 'Hora': arreglo[6]}])
            else: 
                i+=1
        return thejson

    @app.route("/propietario/<conjunto>/<torre>/<piso>/<apartamento>")
    def getPropietario(conjunto, torre, piso, apartamento):
        x = {}
        cursor = collection.find({})
        i = 0
        for document in cursor:
            arreglo = []
            activo = document['Activo'].replace('\\','')
            tipo = document['Tipo'].replace('\\','')
            conjunto = document['Conjunto'].replace('\\','')
            torre = document['Torre'].replace('\\','')
            piso = document['Piso'].replace('\\','')
            apartamento = document['Apartamento'].replace('\\','')
            hora = document['Hora']
            arreglo=[activo, tipo, conjunto, torre, piso, apartamento, str(hora).replace('\\','')]
            if arreglo[2] == (conjunto) and arreglo[3] == (torre) and arreglo[4] == (piso) and arreglo[5] == (apartamento) :
               thejson = json.dumps([{ 'Activo':arreglo[0], 'Tipo':arreglo[1], 'Conjunto': arreglo[2], 'Torre': arreglo[3], 'Piso': arreglo[4], 'Apartamento': arreglo[5], 'Hora': arreglo[6]}])
            i+=1
        return thejson

    
        
    def post(self):
        json_data = request.get_json(force = True)
        activo = json_data['Activo']
        tipo = json_data['Tipo']
        conjunto = json_data['Conjunto']
        torre = json_data['Torre']
        piso = json_data['Piso']
        apartamento = json_data['Apartamento']
        hora = datetime.datetime.utcnow()
        guardar ={
            'Activo' : activo,
            'Tipo' : tipo,
            'Conjunto' : conjunto,
            'Torre' : torre,
            'Piso' : piso,
            'Apartamento' : apartamento,
            'Hora' : hora
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(activo = activo, tipo = tipo, conjunto = conjunto, torre = torre, piso = piso, apartamento = apartamento, hora = hora)                                        
api.add_resource(HelloWorld, '/alertas')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
