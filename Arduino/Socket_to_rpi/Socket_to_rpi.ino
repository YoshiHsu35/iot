/*******************
2015/05/05
Version:1.6.2
Device:
1. Arduino UNO.
2. W5100(Don't need other device or line)

Modify:
1. Add new function about json receive.

1.6.2 Add fast switch address. not modify logic.
1.6 Adjust sending data to GW flow.

Bugs:
1.6.2 Need repair GW->Node Recv issue.

Flow:
1. Send a message to spec address.
2. If the spec address feedback the message, anallys the message and do something.
3. User use the lib of JSON format to send message to GW and Read.

By, Emp,CHEN. Nathaniel,CHEN. KaiRen,KE.

ref:
http://www.arduino.cc/en/Reference/Ethernet
https://github.com/bblanchon/ArduinoJson

*******************/
#define MSG_INTERVAL 1000UL// 500 ms, Unsign Long
#define INT_INTERVAL 2000UL// 1s
#include <ArduinoJson.h>
#include <Ethernet.h>
#include <SPI.h>
#include <String.h>
EthernetClient client;
unsigned long lastTime;

//byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xFD };
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

//char hostname[] = "122.117.119.197";

//char hostname[] = "192.168.1.81";
char hostname[] = "192.168.1.31";

//char Main_Device[] = "D1";
char Main_Device[] = "D2";

int port = 50000;
const int LED_Pin = 4; //LED Pin.
const int Button_Pin = 3; //button pin.
const int interruptNumber = 1; //interrupt 1 on pin 3

bool Receive = false; //For confirm Receive start from '{' to '}' .
bool Finish = false; //For confirm receive finish.
StaticJsonBuffer<200> jsonBuffer;
//char json[] ="{\"Device\":\"D1\",\"Contro\":\"12\",\"data\":[48.756080,2.302038]}";
char* json = "{\"Device\":\"D1\",\"Control\":\"REP\",\"Switch\":\"ON\"}";
String jsonString = jsonString + json;
const char* Com_Device;
const char* Com_Control;
const char* Com_Switch;

String msgString_temp = "";
String Compa_Str1 = "";
String Compa_Str2 = "";
char message[100];

unsigned long now = 0;

//void buttonStateChanged() {
//
//  //蠻怪的，中斷有時候會搞掛mcu
//  Serial.println(digitalRead(Button_Pin));
//  detachInterrupt(interruptNumber);
//  if (client.connected()) {
//    Serial.println("Seding...");
//    client.print(jsonString);
//    Serial.println("Trigger BTN!");
//
//    delay(3000);
//  }
//
//}

void setup() {
  Serial.begin(9600);
  pinMode(Button_Pin, INPUT);
  pinMode(LED_Pin, OUTPUT);
  digitalWrite(Button_Pin, HIGH);
  //attachInterrupt(interruptNumber, buttonStateChanged, HIGH);

  Serial.print("Connecting to GW, please wait.");
  Ethernet.begin(mac);
  if (!client.connect(hostname, port))
  {
    Serial.println(F("Not connected."));
  }
  else
  {
    initREGMSG();
  }

}

void initREGMSG()
{
  StaticJsonBuffer<200> jsonBuffer;
  char jsonCharBuffer[256];

  JsonObject& root = jsonBuffer.createObject();
  root["Device"] = Main_Device;
  root["Control"] = "REG";
  root["TimeStamp"] = lastTime;

  root.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));

  Serial.print("Sending INIT REG MSG...: ");
  Serial.println(jsonCharBuffer);
  client.print(jsonCharBuffer);
}

void loop() {
  now = millis();

  if (client.available()) {
    char c = client.read();
    /*Catch the information if I want*/
    if (Finish == false) {
      if (Receive == false) {
        if (c == '{') {
          msgString_temp += c;
          Receive = true;
        }
      }
      else if (Receive == true) {
        msgString_temp += c;
        if (c == '}') {
          Receive = false;
          Finish = true;
        }
      }
    }



  }

  if ((now - lastTime) >= INT_INTERVAL) {// Send a message between a time interval
    lastTime = now;

    int btn_status = digitalRead(Button_Pin);
    Serial.print("Read Button:");
    Serial.println(btn_status);

    Serial.println("Recv from GW:");
    Serial.print(msgString_temp);

    msgString_temp.toCharArray(message, 100); //Transfer String to char Array.
    Process_SW_info(message);//Receive and process. Store information to spec var.
    Node_Actions();

    if (btn_status == LOW)
    {
      StaticJsonBuffer<200> jsonBuffer;
      char jsonCharBuffer[256];

      JsonObject& root = jsonBuffer.createObject();
      root["Device"] = Main_Device;
      root["Control"] = "REP";
      root["Switch"] = "ON";
      root["TimeStamp"] = lastTime;

      root.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));

      Serial.print("Sending...: ");
      Serial.println(jsonCharBuffer);
      client.print(jsonCharBuffer);
    }

    msgString_temp = "";
    Finish = false;
    Receive = false;

    //檢查有沒有掉線，有的話自動重連
    if (!client.connected())
    {
      Serial.println(F("Reconnectting."));
      client.stop();
      if (!client.connect(hostname, port))
      {
        Serial.println(F("Not connected."));
        client.stop();
      }
      else
      {
        initREGMSG();
      }
    }

    //    Serial.println("RESET INTTERUPT");
    //
    //    attachInterrupt(interruptNumber, buttonStateChanged, HIGH);
  }

}

void Process_SW_info(char* message)
{
  JsonObject& Command = jsonBuffer.parseObject(message);
  Com_Device = Command["Device"].asString();
  Com_Control = Command["Control"].asString();
  Com_Switch = Command["Switch"].asString();
}

void Initial_String(String str1, String str2)
{
  Compa_Str1 = "";
  Compa_Str2 = "";
}

void Node_Actions()
{
  Serial.println(">>>in Node_Actions<<<");

  Serial.println(Com_Switch);
  Serial.println(Com_Control);
  //Node的動作
  if (Com_Switch == "ON" && Com_Control == "SWITCH")
  {
    digitalWrite(LED_Pin, HIGH);
    Serial.println(">>>LED ON<<<");
  }
  else if (Com_Switch == "OFF" && Com_Control == "SWITCH")
  {
    digitalWrite(LED_Pin, LOW);
    Serial.println(">>>LED OFF<<<");
  }
}

