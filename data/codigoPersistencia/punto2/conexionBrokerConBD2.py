from kafka import KafkaConsumer
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


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('Activo.A02.conjunto.1.1.1',
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.81:8090'])

print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    
    json_data = json.loads(message.value.decode('utf-8'))
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
        

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)

# Subscribe to a regex topic pattern
consumer = KafkaConsumer()
consumer.subscribe(pattern='#')
