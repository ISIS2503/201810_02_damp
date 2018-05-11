from kafka import KafkaConsumer
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['connect_to_mongo']
collection = db.horarios

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print(message.payload)

    
    

    
   
 
Connected = False   #global variable for the state of the connection
 
broker_address= "172.24.41.203"  #Broker address
port = 8083                         #Broker port
user = "microcontrolador"                    #Connection username
password = "Isis2503."            #Connection password
topicSub = [("Activo.A3.conjunto.1.1.1",0),("Activo.A4.conjunto.1.1.1",0),
            ("Activo.A5.conjunto.1.1.1",0),("Activo.A6.conjunto.1.1.1",0)]
 
client = mqtt.Client()               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
#client.subscribe("Activo.#.conjunto.*")
client.subscribe(topicSub)

 
try:
    
    while True:
        time.sleep(1)
        #print(client.on_message)
 
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()





