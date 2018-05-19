from kafka import KafkaConsumer
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import time
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['apirestfulencincominutos']
collection = db.alertas

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print(message.payload)
    #for message in client:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
       #                                   message.offset, message.key,
        #                                  message.value))
    
    #json_data = json.loads(message.decode('utf-8'))
    json_data = json.loads(message.payload)
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


 
Connected = False   #global variable for the state of the connection
 
broker_address= "172.24.41.203"  #Broker address
port = 8083                         #Broker port
user = "microcontrolador"                    #Connection username
password = "Isis2503."            #Connection password
topic = [("Activo.A3.conjunto.1.1.1",0),("Activo.A4.conjunto.1.1.1",0),("Activo.A5.conjunto.1.1.1",0),("Activo.A6.conjunto.1.1.1",0)]
 
client = mqtt.Client()               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe(topic)

 
try:
    
    while True:
        time.sleep(1)
        #print(client.on_message)
 
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()





