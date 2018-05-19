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
    
    #json_data = json.loads(message.decode('utf-8'))
    json_data = json.loads(message.payload)
    valor = json_data['Valor']

   
    hoy = datetime.datetime.now()
    ## representacion de fecha y hora
    print("Fecha y hora " + hoy.strftime('%m/%d/%Y'))

    ano = hoy.year
    mes = hoy.month
    dia = hoy.day

    horaHoy = hoy.hour
    print ("Hora = %s" %hoy.hour)

    dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', \
    'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}

 
    fecha = datetime.date(ano, mes, dia)
    diaSemana = (dicdias[fecha.strftime('%A').upper()])
    access = 'ACCESS;false'

    print(diaSemana)

    x = {}
    cursor = collection.find({})
    i = 0
    
    for document in cursor:       
        arreglo = []
        idH = document['idH'].replace('\\','')
        dia = document['Dia'].replace('\\','')
        horaP = document['Hora1'].replace('\\','')
        horaS = document['Hora2'].replace('\\','')
        timeZone = document['TimeZone'].replace('\\','')
        arreglo=[idH, dia, horaP, horaS, timeZone]
        x['Dia#' + str(i)] = arreglo
        i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idH:':v[0], 'Dia:':v[1], 'Hora1:':v[2], 'Hora2:':v[3], 'TimeZone:':v[4]}} for k,v in x.items()])
        
        if (arreglo[1] == (diaSemana) and int(horaHoy) >=  int((horaP)) and int(horaHoy) <= int((horaS))):
                  access = 'ACCESS;true'        

        else: 
             i+=1

    broker_address= "172.24.41.200"  #Broker address
    port = 8083                         #Broker port
    client = mqtt.Client()               #create new instance
    #client.username_pw_set(user, password=password)    #set username and password
    client.on_connect= on_connect                      #attach function to callback
    client.on_message= on_message                      #attach function to callback
 
    client.connect(broker_address, port=port)
    client.connect(broker_address, port=port)          #connect to broker
 
    client.loop_start()        #start the loop
 
    while Connected != True:    #Wait for connection
          time.sleep(0.1)

    print(access)
    client.publish('Activo.A1.conjunto.1.1.1.config', access)
         

    
   
 
Connected = False   #global variable for the state of the connection
 
broker_address= "172.24.41.200"  #Broker address
port = 8083                         #Broker port
#user = "yourUser"                    #Connection username
#password = "yourPassword"            #Connection password
topicSub = [("Activo.A1.conjunto.1.1.1.claves",0)]
topicPub = ("Activo.A1.conjunto.1.1.1.config",0)
 
client = mqtt.Client()               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe(topicSub)

 
try:
    
    while True:
        time.sleep(1)
        #print(client.on_message)
 
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()





