#以下程式將發送信息模組化，並藉由該模組化的程式碼傳送信息給予指定的Topic
__author__ = 'Emp'
import paho.mqtt.client as mqtt
from threading import Thread
class PublisherManager():
    def MQTT_PublishMessage(self,message,topicName):#傳送到指定的Topic上
        print "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (topicName, message)
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(_g_cst_ToMQTTTopicBroker, _g_cst_ToMQTTTopicServerPort)
        mqttc.publish(topicName,message)
        #mqttc.loop(2)