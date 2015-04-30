/*******************
2015/05/01
Version:1.6
Device:
1. Arduino UNO.
2. W5100(Don't need other device or line)

Modify:
1. Add new function about json receive.

1.6 Adjust sending data to GW flow.

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
#include "Socket_to_rpi.h"
EthernetClient client;
unsigned long lastTime;
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
//char hostname[] = "122.117.119.197";
char hostname[] = "192.168.41.64";
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
char message[50];

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
  //attachInterrupt(interruptNumber, buttonStateChanged, HIGH);

Serial.print("Connecting to GW, please wait.");
  Ethernet.begin(mac);
  if (!client.connect(hostname, port)) Serial.println(F("Not connected."));

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

    Serial.println("Recv from GW:");
    Serial.print(message);

    msgString_temp.toCharArray(message, msgString_temp.length() + 1); //Transfer String to char Array.
    Process_SW_info(message);//Receive and process. Store information to spec var.

    Node_Actions();

  }

  if ((now - lastTime) >= INT_INTERVAL) {// Send a message between a time interval
    lastTime = now;
    int btn_status = digitalRead(Button_Pin);
    Serial.print("Read Button:");
    Serial.println(btn_status);


    if (btn_status == HIGH)
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
  //Node的動作

}

