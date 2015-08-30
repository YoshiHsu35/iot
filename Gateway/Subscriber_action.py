#!/usr/bin/python
# -*- coding: utf-8 -*-

# 該篇程式主要用途在於註冊動作的模組化

__author__ = 'Emp'
from threading import Thread
import paho.mqtt.client as mqtt
import sys
import json
import time

# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


class SubscriberThreading(Thread):  # 宣告一Class，並在每次呼叫到時創建一個Thread，讓註冊後的通道能夠不間斷的接收在上面的信息
    global topicName

    def __init__(self, topicName):  # 本位寫法，請注意Python中Address的部分，有些指定位置會在同一個地方
        Thread.__init__(self)
        self.topicName = topicName

    def run(self):  # Use run to create Thread. Run是預設的Function
        subscriberManager = SubscriberManager()
        subscriberManager.subscribe(self.topicName)


class SubscriberManager():
    def subscribe(self, topicName):
        self.topicName = topicName
        ########## MQTT Subscriber ##############
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print("[INFO] Connected MQTT Topic Server:" + self.topicName + " with result code " + str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            # print(type(self.topicName))
            client.subscribe(topicName)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print("[INFO] MQTT message receive from Topic %s at %s :%s" % (
                msg.topic, time.asctime(time.localtime(time.time())), str(msg.payload)))
            try:
                _obj_json_msg = json.loads(msg.payload)
                from Gateway.Gateway import RoutingNode
                RoutingNode(_obj_json_msg)
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
        print("[INFO] Subscribe TopicName:" + topicName)
        client.loop_forever()
