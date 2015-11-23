#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

import time
import json
import copy
import sys
import class_Node_MQTTManager
from terminalColor import bcolors
import class_Node_Obj
import uuid

_g_cst_NodeUUID = "NODE-01"
# _g_cst_NodeUUID ="NODE-" +uuid.uuid1()

_g_cst_MQTTRegTopicName = "IOTSV/REG"  # GW一開始要和IoT_Server註冊，故需要傳送信息至指定的MQTT Channel
_g_Functions = ["LED1", "LED2", "SW1"]

print("::::::::::::::::::::::::::::::::::::::::::\n")
print("::::::::::::::::::::::::::::::::::::::::::\n")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
    print("线程名：　" + threading.current_thread().getName())

    _b_MQTTConnected = False
    global publisher
    publisher = class_Node_MQTTManager.PublisherManager()
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % _g_cst_NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        initMSGObj = {'Node': _g_cst_NodeUUID, 'Control': 'NODE_REG', 'NodeFunctions': ['IOs', 'IPCams'],
                      'Functions': ["LED1", "LED2", "SW1"], 'Source': _g_cst_NodeUUID}
        initMSGSTR = json.dumps(initMSGObj)

        class_Node_MQTTManager.SubscriberThreading(_g_cst_MQTTRegTopicName).start()
        # 訂閱自身名稱的topic
        class_Node_MQTTManager.SubscriberThreading(_g_cst_NodeUUID).start()

        publisher.MQTT_PublishMessage(_g_cst_MQTTRegTopicName, initMSGSTR)

        _b_MQTTConnected = True
    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


Rules = []


########### Normal Socket to Server(As socket client) ##############
def RxRouting(_obj_json_msg):
    global publisher
    publisher = class_Node_MQTTManager.PublisherManager()
    separation_obj_json_msg = copy.copy(_obj_json_msg)
    if separation_obj_json_msg["Control"] == "ADDFS":  # Recive control from IoT Server for Function Server Topic
        for fp in separation_obj_json_msg["FSPairs"]:

            # ["FS1", "M2M", "10.0.0.1", "IOs"]
            fspair = class_Node_Obj.FSPair(fp[0], fp[1], fp[2], fp[3])

            if (fp[1] == "M2M"):
                try:
                    ReqToFS = {"Node": "%s" % _g_cst_NodeUUID, "Control": "M2M_REQTOPICLIST",
                               "Source": "%s" % _g_cst_NodeUUID}
                    Send_json = json.dumps(ReqToFS)
                    publisher.MQTT_PublishMessage(fp[0], Send_json)
                    class_Node_MQTTManager.SubscriberThreading(fp[0]).start()
                except (RuntimeError, TypeError, NameError) as e:
                    print(bcolors.FAIL + "[ERROR] Send Request for topic list error!" + str(e) + bcolors.ENDC)
                    return
    elif separation_obj_json_msg["Control"] == "M2M_REPTOPICLIST":
        for subTopic in separation_obj_json_msg["SubscribeTopics"]:
            RuleObj = class_Node_Obj.M2M_RuleObj(subTopic["TopicName"], subTopic["Target"],
                                                 subTopic["TargetValueOverride"])

            Rules.append(RuleObj)
            class_Node_MQTTManager.SubscriberThreading(subTopic["TopicName"]).start()

    elif separation_obj_json_msg["Control"] == "M2M_SET":
        for rule in Rules:
            if rule.TopicName == separation_obj_json_msg["TopicName"]:
                print(
                    bcolors.OKGREEN + ">>Trigger<< Rx SET Msg " + rule.Target + " " + rule.TargetValueOverride + bcolors.ENDC)


if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="my")
    MQTT_Thread.start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
