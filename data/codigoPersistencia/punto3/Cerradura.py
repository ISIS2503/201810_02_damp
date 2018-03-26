from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['connect_to_mongo']
collection = db.CERRADURAS

class TodoList(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        idP = json_data['idP']
        informacion = json_data['Informacion']
        guardar ={
            'idP' : idP,
            'Informacion' : informacion
            }
        collection.insert_one(guardar).inserted_id
        return jsonify(idP = idP, Informacion = informacion)
    def get(self):
        x = {}
        cursor = collection.find({})
        i = 1
        for document in cursor:
            arreglo = []
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
            x['Cerradura#' + str(i)] = arreglo
            i+=1
        thejson = json.dumps([{k :{ 'idP':v[0], 'Informacion':v[1]}} for k,v in x.items()])
        return thejson
class Todo(Resource):
    def get(self, idP):
        arreglo = []
        cursor = collection.find({"idP": (idP)})
        for document in cursor:
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
        else:
            thejson=[]
        return thejson
    def put(self, idP):
        json_data = request.get_json(force = True)
        informacion = json_data['Informacion']
        collection.update_one(
                {'idP' : idP},
                {"$set": {'Informacion': informacion}},
                upsert=False
            )
        return jsonify(idP = idP, Informacion = informacion)
    def delete(self, idP):
        arreglo = []
        cursor = collection.find({"idP": (idP)})
        try:
            for document in cursor:
                idP = document['idP'].replace('\\','')
                informacion = document['Informacion'].replace('\\','')
                arreglo=[idP, informacion]
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
            collection.remove({"idP": idP})
            return thejson
        except:
            print ("No se encuentra el idP en la BD")
api.add_resource(TodoList, '/cerraduras')
api.add_resource(Todo, '/cerraduras/<idP>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)

