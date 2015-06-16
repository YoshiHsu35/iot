#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import paho.mqtt.client as mqtt
import time
import json
import copy
import sys
import class_Subscriber

#上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


print("::::::::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::::::::")
print("'####::'#######::'########::'######::'##::::'##:")
print(". ##::'##.... ##:... ##..::'##... ##: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##:::: ##:::..:: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##::::. ######:: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##:::::..... ##:. ##:: ##::")
print(": ##:: ##:::: ##:::: ##::::'##::: ##::. ## ##:::")
print("'####:. #######::::: ##::::. ######::::. ###::::")
print("....:::.......::::::..::::::......::::::...:::::")
print("::::::::::::::::::::::::::::::::::::::::::::::::\n")




def main():
    subscriberManager = class_Subscriber.SubscriberManager()
    subscriberManager.MQTT_SubscribeTopic("IOTSV/REG")


if __name__ == '__main__':
        main()



########### MQTT Publisher ##############

def MQTT_PublishMessage(topicName,message):
    print "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (topicName, message)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort)
    mqttc.publish(topicName,message)
    mqttc.loop(2)  #timeout 2sec



# TODO
def DecisionAction(_obj_json_msg):
    spreate_obj_json_msg = copy.copy(_obj_json_msg)
    if (spreate_obj_json_msg["Gateway"]=="_g_cst_gatewayName"):
        global _g_nodeList

        isSendNodeSuccess = False

        for node_client in _g_nodeList:

            if(node_client[1]==spreate_obj_json_msg["Device"]):
                #轉成文字
                _str_sendToGWJson = json.dumps(spreate_obj_json_msg)
                print "Ready to transport message is: %s" % _str_sendToGWJson

                try:
                    node_client[0].send(_str_sendToGWJson)
                    isSendNodeSuccess = True
                except:
                    print "[ERROR] send to node have some error!"
                    isSendNodeSuccess = False

        if not isSendNodeSuccess:
            print "Destination Node:%s didn't online" % spreate_obj_json_msg["Device"]

    else:
        print "[INFO] Receive message in wrong GW name!"