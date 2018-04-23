#include <Keypad.h>
#include <EEPROM.h>

//VERSION FINAL
#define SIZE_BUFFER_DATA       50
boolean     stringComplete = false;
String      inputString = "";
char        bufferData [SIZE_BUFFER_DATA];

//Minimum voltage required for an alert
const double MIN_VOLTAGE = 1.2;

//Battery indicator
const int BATTERY_LED = 11;

//Battery measure pin
const int BATTERY_PIN = A2;

//Current battery charge
double batteryCharge;

boolean low;

boolean sound;

long currTimeLow;

long currTimeSound;

const int BUZZER_BATTERY = A4;

//Specified password
const int claves = 4;
const String KEY[claves] = {"1234" , "2223" , "3456", "4444"};
const int keySize = 4;

//Time in milliseconds which the system is locked
const int LOCK_TIME = 30000;

//Keypad rows
const byte ROWS = 4;

//Keypad columns
const byte COLS = 3;

//Maximum number of attempts allowed
const byte maxAttempts = 3;

//Keypad mapping matrix
char hexaKeys[ROWS][COLS] = {
  {
    '1', '2', '3'
  }
  ,
  {
    '4', '5', '6'
  }
  ,
  {
    '7', '8', '9'
  }
  ,
  {
    '*', '0', '#'
  }
};

//Keypad row pins definition
byte rowPins[ROWS] = {
  3, 4, 5, 6
};

//Keypad column pins definition
byte colPins[COLS] = {
  7, 8, 9
};

//Keypad library initialization
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

//Current key variable
String currentKey;

//If the number of current attempts exceeds the maximum allowed
boolean block;

int analogPin = 3;     // potentiometer wiper (middle terminal) connected to analog pin 3
int ledPin = 2;                       // outside leads to ground and +5V
int val = 0;           // variable to store the value read
//  setup serial
int pirState = LOW;



//Button pin
const int CONTACT_PIN = 11;

//R LED pin
const int R_LED_PIN = 13;

//G LED pin
const int G_LED_PIN = 12;

//B LED pin
const int B_LED_PIN = 10;

//Door state
boolean open;

//Attribute that defines the button state
boolean buttonState;

//Current time when the button is tapped
long currTime;

//Number of current attempts
byte attempts;

void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(BUZZER_BATTERY, OUTPUT);

  buttonState = false;

  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN, INPUT);

  currentKey = "";  
  open = false;
  attempts = 0;
  block = false;

  analogWrite(R_LED_PIN, 0);
  analogWrite(G_LED_PIN, 255);
  analogWrite(B_LED_PIN, 255);

  // Ouput pin definition for BATTERY_LED
  pinMode(BATTERY_LED, OUTPUT);

  //Input pin definition for battery measure
  pinMode(BATTERY_PIN, INPUT);
}

void loop()
{


        
  //Value conversion from digital to voltage
  batteryCharge = (analogRead(BATTERY_PIN) * 5.4) / 1024;

  //Measured value comparison with min voltage required
  if (batteryCharge <= MIN_VOLTAGE) {
    digitalWrite(BATTERY_LED, HIGH);
    //Serial.println("LOW BATTERY");
    Serial.println("A/4");
    //Serial.println(currTimeLow);
    //Serial.println(currTimeSound);
    if (!low)
    {
      low = true;
      currTimeLow = millis();
    }


    if ((millis() - currTimeLow) >= 30000) {

      digitalWrite(BUZZER_BATTERY, HIGH);
      if (!sound) {
        sound = true;
        currTimeSound = millis();
      }
      currTimeLow = millis();
    }

    if ((millis() - currTimeSound) >= 2000) {
      digitalWrite(BUZZER_BATTERY, LOW);
      sound = false;
      currTimeSound = millis();
    }
  }
  else {
    digitalWrite(BATTERY_LED, LOW);
    low = false;
  }
  //Button input read and processing
  if (!buttonState)
  {
    if (analogRead(1) > 500) {
      currTime = millis();
      buttonState = true;
      setColor(0, 0, 255);
      open = true;
      attempts = 0;
      //Serial.println("Door opened!!");
    }
  }
  else {
    if (analogRead(1) > 500) {
      if ((millis() - currTime) >= 30000) {
        setColor(255, 0, 0);
        currTime = millis();
        Serial.println("A/1");
      }
    } else {
      if (analogRead(1) > 500) {
        open = true;
      } else {
        open = false;
        buttonState = false;
        setColor(0, 255, 255);
        //Serial.println("Door closed!!");
      }
    }
  }

  val = analogRead(analogPin);     // read the input pin
  if (val > 670) {           // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("A/2");
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH) {
      // we have just turned of
      Serial.println("A/2");
      // We only want to print on the output change, not state
      pirState = LOW;
    }// debug value
  }


  char customKey;

  if (!block) {
    //Selected key parsed;
    customKey = customKeypad.getKey();
  }
  else {
    Serial.println("A/3");
    while (true);
  }

  //Verification of input and appended value
  if (customKey) {
    currentKey += String(customKey);
    Serial.println(currentKey);
  }

  //If the current key contains '*' and door is open
  if (open && currentKey.endsWith("*")) {
    open = false;
    setColor(0, 255, 255);
    Serial.println("Door closed");
    digitalWrite(10, LOW);
    currentKey = "";
    currTime = millis();
    check();
  }
  //If the current key contains '#' reset attempt
  if (currentKey.endsWith("#") && currentKey.length() <= keySize) {
    currentKey = "";
    //Serial.println("Attempt deleted");
  }

  //If current key matches the key length
  if (currentKey.length() == keySize)
  {
    int i = 0;
    boolean centinela = false;
    while (i < claves && centinela == false) {

      if (currentKey == KEY[i] && !((millis() - currTime) >= 30000))
      {
        digitalWrite(10, HIGH);
        open = true;
        centinela = true;
        Serial.println("Door opened!!");
        check();
        attempts = 0;
        i = claves;
      }
      else if (currentKey != KEY[i]) {
        i++;
      }
      else if (currentKey == KEY[i] && ((millis() - currTime) >= 30000))
      {
        digitalWrite(10, HIGH);
        open = true;
        centinela = true;
        check();
        attempts = 0;
        i = claves;
      }

    }
    if (i == claves && centinela == false) {
      attempts++;
      currentKey = "";
      setColor(255, 0, 0);
      delay(1000);
      setColor(0, 255, 255);
      Serial.println("Number of attempts: " + String(attempts));
      if (attempts >= maxAttempts)
      {

        Serial.println("A/3");
        setColor(255, 0, 0);
        delay(LOCK_TIME);
        setColor(0, 255, 255);
        attempts = 0;
        currTime = millis();
      }
    }
  }
}

//Method that outputs the RGB specified color
void check() {
  if (open == true && (millis() - currTime) >= 30000)
  {
    setColor(255, 0, 0);
    Serial.println("A/1");
  }
  else if (open == true && !((millis() - currTime) >= 30000))
  {
    setColor(0, 0, 255);
  }
  else if (open == false)
  {
    setColor(0, 255, 255);
    currTime = millis();
  }
}
void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}


// Method that compares a key with stored keys
boolean compareKey(String key) {
  int acc = 3;
  int codif, arg0, arg1; 
  for(int i=0; i<3; i++) {
    codif = EEPROM.read(i);
    while(codif!=0) {
      if(codif%2==1) {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc+1)*256;
        arg1+= arg0;
        if(String(arg1)==key) {
          return true;
        }
      }
      acc+=2;
      codif>>=1;
    }
    acc=(i+1)*16+3;
  }
  return false;
}

// Methods that divides the command by parameters
void processCommand(String* result, String command) {
  char buf[sizeof(command)];
  String vars = "";
  vars.toCharArray(buf, sizeof(buf));
  char *p = buf;
  char *str;
  int i = 0;
  while ((str = strtok_r(p, ";", &p)) != NULL) {
    // delimiter is the semicolon
    result[i++] = str;
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location,j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index) {
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location,j);
}

//Method that deletes all passwords
void deleteAllPasswords() {
  //Password reference to inactive
  EEPROM.write(0,0);
  EEPROM.write(1,0);
  EEPROM.write(2,0);
}

void receiveData() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
    }
  }
}
 
void processData() {
  if (stringComplete) {
    String* result;
    processCommand(result,inputString);
    String comando=result[0];
    if(comando.equals("ADD_PASSWORD")){
      //ADD_PASSWORD;<index>;<newPassword>
      addPassword(result[2].toInt(),result[1].toInt());
    }else if(comando.equals("UPDATE_PASSWORD")){
      //UPDATE_PASSWORD;<index>;<newPassword>
      updatePassword(result[2].toInt(),result[1].toInt());
    }else if(comando.equals("DELETE_PASSWORD")){
      //DELETE_PASSWORD;<index>
      deletePassword(result[1].toInt());
    }else if(comando.equals("DELETE_ALL")){
      //DELETE_ALL
      deleteAllPasswords();
    }else if(comando.equals("COMPARE_KEY")){
      //COMPARE_KEY;<key>
      compareKey(result[1]);
    }
  }
}
