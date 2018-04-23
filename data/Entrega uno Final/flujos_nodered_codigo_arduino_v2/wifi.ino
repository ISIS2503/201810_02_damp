#include <PubSubClient.h>
#include <ESP8266WiFi.h>

//DEFINES
#define TOPIC_SUBSCRIBEA1        "Activo.A1.conjunto.1.1.1.config"
#define TOPIC_PUBLISHA1          "Activo.A1.conjunto.1.1.1"

#define TOPIC_SUBSCRIBEA2        "Activo.A2.conjunto.1.1.1.config"
#define TOPIC_PUBLISHA2          "Activo.A2.conjunto.1.1.1"

#define TOPIC_SUBSCRIBEA3        "Activo.A3.conjunto.1.1.1.config"
#define TOPIC_PUBLISHA3          "Activo.A3.conjunto.1.1.1"

#define TOPIC_SUBSCRIBEA4        "Activo.A4.conjunto.1.1.1.config"
#define TOPIC_PUBLISHA4          "Activo.A4.conjunto.1.1.1"

#define SIZE_BUFFER_DATA       50

//VARIABLES

#define TOPIC_SUBSCRIBEA0  "Activo.A0.conjunto.1.1.1.config"
#define TOPIC_PUBLISHA0 "Activo.A0.conjunto.1.1.1"


int alarma = 0;

const char* idDevice = "ISIS2503";
boolean     stringComplete = false;
boolean     init_flag = false;
String      inputString = "";
char        bufferData [SIZE_BUFFER_DATA];

// CLIENTE WIFI & MQTT`
WiFiClient    clientWIFI;
PubSubClient  clientMQTT(clientWIFI);

// CONFIG WIFI
const char* ssid = "isis2503";
const char* password = "Yale2018.";

// CONFIG MQTT
IPAddress serverMQTT (172,24,41,200);
const uint16_t portMQTT = 8083;
// const char* usernameMQTT = "admin";
// const char* passwordMQTT = "admin";

void connectWIFI() {
  // Conectar a la red WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void reconnectWIFI() {
  // Conectar a la red WiFi
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.write(payload, length);
  Serial.println();
}

void setup() {
  Serial.begin(9600);
  inputString.reserve(100);

  clientMQTT.setServer(serverMQTT, portMQTT);
  clientMQTT.setCallback(callback);
  connectWIFI();
  delay(1000);
}

void processData() {
  if (WiFi.status() == WL_CONNECTED) {
    if(init_flag == false) {
      init_flag = true;

      boolean conectMQTT = false;
      if (!clientMQTT.connected()) {
        // if (!clientMQTT.connect(idDevice, usernameMQTT, passwordMQTT)) {
        if (!clientMQTT.connect(idDevice)) {
          conectMQTT = false;
        }
        conectMQTT = true;
      }
      else {
        conectMQTT = true;
      }

      if(conectMQTT) {
        if(alarma==0){ 
          if(clientMQTT.subscribe(TOPIC_SUBSCRIBEA0)) {
           Serial.println("Subscribe OK");
          }
        }else if(alarma==1){
          if(clientMQTT.subscribe(TOPIC_SUBSCRIBEA1)) {
           Serial.println("Subscribe OK");
          }
        }else if(alarma==2){
          if(clientMQTT.subscribe(TOPIC_SUBSCRIBEA2)) {
           Serial.println("Subscribe OK");
          }
        }else if(alarma==3){
          if(clientMQTT.subscribe(TOPIC_SUBSCRIBEA3)) {
           Serial.println("Subscribe OK");
          }
        }else if(alarma==4){
          if(clientMQTT.subscribe(TOPIC_SUBSCRIBEA4)) {
           Serial.println("Subscribe OK");
          }
        }
      }
    }

    if (stringComplete && clientMQTT.connected()) {
      if(alarma==0){ 
          if(clientMQTT.publish(TOPIC_PUBLISHA0, bufferData)) {
            inputString = "";
            stringComplete = false;
          }
        }else if(alarma==1){
          if(clientMQTT.publish(TOPIC_PUBLISHA1, bufferData)) {
            inputString = "";
            stringComplete = false;
          }
        }else if(alarma==2){
          if(clientMQTT.publish(TOPIC_PUBLISHA2, bufferData)) {
            inputString = "";
            stringComplete = false;
          }
        }else if(alarma==3){
          if(clientMQTT.publish(TOPIC_PUBLISHA3, bufferData)) {
            inputString = "";
            stringComplete = false;
          }
        }else if(alarma==4){
          if(clientMQTT.publish(TOPIC_PUBLISHA4, bufferData)) {
            inputString = "";
            stringComplete = false;
          }
        }
      init_flag = false;
    }
  }
  else {
    connectWIFI();
    init_flag = false;
  }
  clientMQTT.loop();
}

void receiveData() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
    }
  }
}

void loop() {
  receiveData();
  processData();
}
