#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import paho.mqtt.client as mqtt
import time
import json
import copy
import sys


#上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


class SubscriberManager():


    ########## MQTT Subscriber ##############

    def MQTT_SubscribeTopic(self,topicName):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("[INFO] Connected MQTT Topic Server:"+ topicName +" with result code "+str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe(topicName)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print("[INFO] MQTT message receive from Topic %s at %s :%s" %(msg.topic,time.asctime(time.localtime(time.time())), str(msg.payload)))

            try:
                  print("Hello~~~ %s" % msg.payload)
                #_obj_json_msg = json.loads(msg.payload)

               # DecisionAction(_obj_json_msg)
            except:
                print("[ERROR] Couldn't converte json to Objet!")

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()