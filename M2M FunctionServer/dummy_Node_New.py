__author__ = 'Nathaniel'
import class_M2MFS_MQTTManager
import threading
import json
import time
import uuid

_g_NodeUUID = uuid.uuid1()


def initREG():
    publisherManager = class_M2MFS_MQTTManager.PublisherManager()
    initMSGObj = {'Node': "NODE-" + str(_g_NodeUUID), 'Control': 'NODEREG', 'NodeFunctions': ['IOs'],
                  'Functions': ["LED1", "LED2", "SW1"], 'Source': "NODE-" + str(_g_NodeUUID)}
    initMSGSTR = json.dumps(initMSGObj)
    now = time.strftime("%c")
    print(now)
    print("[INFO] SendREGMSG:%s" % initMSGSTR)
    publisherManager.MQTT_PublishMessage("IOTSV/REG", initMSGSTR)


def main():
    initREG()


if __name__ == '__main__':
    main()
