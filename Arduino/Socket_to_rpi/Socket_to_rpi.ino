/*******************
2015/06/24
Version:2.0

Modify:
1. Follow the Spec for drive Device(LDE,Motor...)
2. 

Next step:
1. None

Bugs:
1. None.

Flow:
1. Send a message to spec address.
2. If the spec address feedback the message, anallys the message and do something.
3. User use the lib for JSON format processing to send message to GW and Read.

By, Emp,CHEN. Nathaniel,CHEN.
ref:
http://www.arduino.cc/en/Reference/Ethernet
https://github.com/bblanchon/ArduinoJson
*******************/
#include <ArduinoJson.h>
#include <Ethernet.h>
#include <SPI.h>
#include <String.h>
#define INT_INTERVAL  1000
EthernetClient client;
unsigned long lastTime;
//--mac number--
//byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xFD };//N1
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };//N2

//--Host name(IP) and port number--
//char hostname[] = "122.117.119.197";
char hostname[] = "192.168.41.85";
//int port = 10000;//GW1
int port = 10010;//GW2

//--Node name--
//char Main_Node[] = "N1";
char Main_Node[] = "N2";

//--Peripheral define--
int LED_Pin = 4; //LED Pin.
int Button_Pin = 3; //button pin.
int interruptNumber = 1; //interrupt 1 on pin 3

//--Flag--
bool Receive = false; //For confirm Receive start from '{' to '}' .
bool Finish = false; //For confirm receive finish.

const char* Node_function;
const char* Com_Control;
const char* Com_Target;
const char* Com_Value;

String msgString_temp = "";//Use that for receive message.

/****String value for char-pointer(s) compare****/
String Compa_Str1 = "";
String Compa_Str2 = "";
String Compa_Str3 = "";
String Compa_Str4 = "";
/***********************************************/

char message[200];
char jsonCharBuffer[256];
unsigned long now = 0;

void setup() {
  Serial.begin(115200);
  pinMode(Button_Pin, INPUT);
  pinMode(LED_Pin, OUTPUT);
  digitalWrite(Button_Pin, HIGH);
  //attachInterrupt(interruptNumber, buttonStateChanged, HIGH);
  Serial.print("Connecting to GW, please wait.");
  Ethernet.begin(mac);
  if (!client.connect(hostname, port))
	  Serial.println(F("Not connected."));
  else{
    initREGMSG();
    delay(2000);//Delay some time for register complete
  }
}
void initREGMSG(){
  StaticJsonBuffer<100> REG_msg_buffer;
  char jsonCharBuffer[256];
  
  JsonObject& root = REG_msg_buffer.createObject();
  root["Node"] = Main_Node;
  root["Control"] = "REG";
  root["NodeFunction"] = Node_function;
  JsonArray& IOs = root.createNestedArray("Functions");
  if(Main_Node[1]=='1'){//If the device is Node1
    IOs.add("LED1");
    IOs.add("LED2");
    IOs.add("SW1");
  }
  else if(Main_Node[1]=='2'){//If the device is Node2
    IOs.add("LED3");
    IOs.add("LED4");
    IOs.add("SW2");
  }
  root.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));
  Serial.print("Sending initial register Message...: ");
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
    Trans_msg["Node"] = Main_Node;
    Trans_msg["Control"] = "REP";
    Trans_msg["Component"] = "SW1";
    digitalWrite(Button_Pin, HIGH);
    Serial.print("Read Button:");
    int Button_state = digitalRead(Button_Pin);
    Serial.println(Button_state);
    Serial.println("Recv from GW:");
    msgString_temp.toCharArray(message, 200); //Transfer String to char-Array.
    Process_SW_info(message);//Receive and process. Store information to specify value.
    Node_Actions();
    
    if(Button_state == LOW){
      Trans_msg["Value"] ="1";
      Trans_msg.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));
      client.print(jsonCharBuffer);
    }
    else{
      Trans_msg["Value"] ='0';
      Trans_msg.printTo(jsonCharBuffer, sizeof(jsonCharBuffer));
    }
      Serial.print("Sending...: ");
      Serial.println(jsonCharBuffer);
      msgString_temp = "";
      Finish = false;//Initial the flag of receive message
      Receive = false;//Initial the flag of receive message
      Reconnecting_Check();//檢查有沒有掉線，有的話自動重連
    //    Serial.println("RESET INTTERUPT");
    //    attachInterrupt(interruptNumber, buttonStateChanged, HIGH);
  }
}
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
  Com_Target = Command["Target"];
  Com_Control = Command["Control"];
  Com_Value = Command["Value"];
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
  Compa_Str1+=Com_Target;
  Compa_Str2+=Com_Value;
  //Serial.println(Com_Switch);
  //Serial.println(Com_Control);
  if (Compa_Str2=="1")
  {
    digitalWrite(LED_Pin, HIGH);
    Serial.println(">>>LED ON<<<");
  }
  else if (Compa_Str2 == "0")
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
