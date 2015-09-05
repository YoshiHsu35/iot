#!/usr/bin/python
# -*- coding: utf-8 -*-


# 以下程式將發送信息模組化，並藉由該模組化的程式碼傳送信息給予指定的Topic
__author__ = 'Emp'
import paho.mqtt.client as mqtt
from terminalColor import bcolors
import config_ServerIPList


class PublisherManager():
    def MQTT_PublishMessage(self, topicName, message):  # 傳送到指定的Topic上
        print(bcolors.WARNING + "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (
            topicName, message) + bcolors.ENDC)
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(config_ServerIPList._g_cst_ToMQTTTopicServerIP, int(
            config_ServerIPList._g_cst_ToMQTTTopicServerPort))
        mqttc.publish(topicName, message)
        mqttc.loop(2)
