/*******************
2015/05/17
Version:1.8
Device:
1. Arduino UNO.
2. W5100(Don't need other device or line)
3. Others.(Button and LEDs)
Modify:
1. Add new function about json receive.
2. Create three object of json that used a memory address for storing.

1.6.2 Add fast switch address. not modify logic.
1.6 Adjust sending data to GW flow.

1.7 Correct transfer message problem from GW2.

Bugs:
1. None.

Flow:
1. Send a message to spec address.
2. If the spec address feedback the message, anallys the message and do something.
3. User use the lib for JSON format processing to send message to GW and Read.

By, Emp,CHEN. Nathaniel,CHEN. KaiRen,KE.
ref:
http://www.arduino.cc/en/Reference/Ethernet
https://github.com/bblanchon/ArduinoJson
*******************/
#include <ArduinoJson.h>
#include <Ethernet.h>
#include <SPI.h>
#include <String.h>
#include "Socket_to_rpi.h"
EthernetClient client;
unsigned long lastTime;
//--mac number--
//byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xFD };//D1
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };//D2

//--Host name(IP) and port number--
//char hostname[] = "122.117.119.197";
char hostname[] = "192.168.41.38";
//int port = 10000;//GW1
int port = 10010;//GW2

//--Device name--
//char Main_Device[] = "D1";
char Main_Device[] = "D2";

//--Peripheral define--
int LED_Pin = 4; //LED Pin.
int Button_Pin = 3; //button pin.
int interruptNumber = 1; //interrupt 1 on pin 3

//--Flag--
bool Receive = false; //For confirm Receive start from '{' to '}' .
bool Finish = false; //For confirm receive finish.

char* json = "{\"Device\":\"D1\",\"Control\":\"REP\",\"Switch\":\"ON\"}";
String jsonString = jsonString + json;
const char* Com_Control;
const char* Com_Switch;
const char* Com_Device;
long Com_time;
const char* Com_Gateway;
const char* Com_Server;

String msgString_temp = "";//Use that for receive message.
/****String value for char-pointer(s) compare****/
String Compa_Str1 = "";
String Compa_Str2 = "";
String Compa_Str3 = "";
String Compa_Str4 = "";

char message[200];
char jsonCharBuffer[256];

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
//    delay(3000);
//  }
//}

void setup() {
  Serial.begin(115200);
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
  StaticJsonBuffer<100> Ini_msg_buffer;
  char jsonCharBuffer[256];
  JsonObject& root = Ini_msg_buffer.createObject();
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
  Receive_Gateway();//Receive from Gateway
  if ((now - lastTime) >= INT_INTERVAL) {// Send a message per second.
    lastTime = now;
    StaticJsonBuffer<100> Trans_Buffer;
    JsonObject& Trans_msg = Trans_Buffer.createObject();
    Trans_msg["Device"] = Main_Device;
    Trans_msg["Control"] = "REP";
    digitalWrite(Button_Pin, HIGH);
    Serial.print("Read Button:");
    int Button_state = digitalRead(Button_Pin);
    Serial.println(Button_state);
    Serial.println("Recv from GW:");
    msgString_temp.toCharArray(message, 200); //Transfer String to char-Array.
    Process_SW_info(message);//Receive and process. Store information to specify value.
    Node_Actions();
    
    if(Button_state == LOW){
      Trans_msg["Switch"] = "ON";
      Trans_msg["TimeStamp"] = lastTime;
      Trans_msg.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));
    }
    else{
      Trans_msg["Switch"] = "OFF";
      Trans_msg["TimeStamp"] = lastTime;
      Trans_msg.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));
    }
      Serial.print("Sending...: ");
      Serial.println(jsonCharBuffer);
      client.print(jsonCharBuffer);
      msgString_temp = "";
      Finish = false;//Initial the flag of receive message
      Receive = false;//Initial the flag of receive message
      Reconnecting_Check();//檢查有沒有掉線，有的話自動重連
    //    Serial.println("RESET INTTERUPT");
    //    attachInterrupt(interruptNumber, buttonStateChanged, HIGH);
  }
}
#include "Socket_to_rpi.h"
void Process_SW_info(char* message_temp)
{
  StaticJsonBuffer<100> Receive_buffer;
  char temp1[200];
  for(int i=0;i<sizeof(temp1);i++)
    temp1[i]=message_temp[i];
  JsonObject& Command = Receive_buffer.parseObject(temp1); 
  if (!Command.success())//Check object.
  {
    Serial.println("parseObject() failed");
    return;
  }
  Com_Switch = Command["LED"];
  Com_Control = Command["Control"];
  Com_Device = Command["Device"];
  Com_time = Command["TimeStamp"];
  Com_Gateway = Command["Gateway"];
  Com_Server = Command["Server"];
}

void Initial_String(void)
{
  Compa_Str1 = "";
  Compa_Str2 = "";
}

void Node_Actions()
{
  //Node的動作
  Serial.println(">>>in Node_Actions<<<");
  //Serial.println(Com_Switch);
  //Serial.println(Com_Control);
  Compa_Str1+=Com_Switch;
  Compa_Str2+=Com_Control;
  //Serial.println(Com_Switch);
  //Serial.println(Com_Control);
  if (Compa_Str1=="ON")
  {
    digitalWrite(LED_Pin, HIGH);
    Serial.println(">>>LED ON<<<");
  }
  else if (Compa_Str1 == "OFF" && Compa_Str2 == "SET")
  {
    digitalWrite(LED_Pin, LOW);
    Serial.println(">>>LED OFF<<<");
  }
  Initial_String();
}
void Receive_Gateway()
{
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
}
void Reconnecting_Check()
{
    if (!client.connected())
    {
      Serial.println(F("Reconnectting."));
      client.stop();
      if (!client.connect(hostname, port)){
        Serial.println(F("Not connected."));
        client.stop();
      }
      else{
        initREGMSG();
      }
    }
}