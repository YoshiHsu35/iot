#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_Obj
import class_MQTTManager
import json
from terminalColor import bcolors

# 看到NodeFunction名為IOs的，代表該Node的訊息要Mapping到M2M的FS，他的TOPIC為FS1
_g_FunctionServerMappingList = [{"FunctionTopic": "FS1", "Function": "M2M", "NodeFunction": "IOs"},
                                {"FunctionTopic": "FS2", "Function": "Streaming", "NodeFunction": "IPCams"}]


class FunctionServerMappingRules():
    def __init__(self):
        self.jsonObj = class_Obj.JSON_ADDFSIP()

    def replyFSTopicToGW(self, topicName, GWObj):
        self.jsonObj.Control = "ADDFSIP"
        for fsMappingRule in _g_FunctionServerMappingList:

            IsFSHaveNodeMapping = False

            #### ASSIGN TO M2M FS ####
            self.FSIP = class_Obj.FSIPObj()
            self.FSIP.FunctionTopic = fsMappingRule["FunctionTopic"]  # FS1
            self.FSIP.Function = fsMappingRule["Function"]  # M2M
            self.FSIP.IP = "0.0.0.0"
            self.FSIP.Nodes = []

            for nodeObj in GWObj:

                if (nodeObj.NodeFunction == fsMappingRule["NodeFunction"]):  # IOs
                    self.FSIP.Nodes.append(nodeObj.NodeUUID)
                    IsFSHaveNodeMapping = True

            # 如果規則中的function在GW下面的Node找不到，則不需要回傳該function所要的topic
            if (IsFSHaveNodeMapping):
                self.jsonObj.FSIPs.append(self.FSIP)

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] ADDFSIP Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyFSTopicToMANAGEDEV(self, topicName):

        for fsMappingRule in _g_FunctionServerMappingList:
            IsFSHaveNodeMapping = False

            #### ASSIGN TO M2M FS ####
            self.FSIP = class_Obj.FSIPObj()
            self.FSIP.FunctionTopic = fsMappingRule["FunctionTopic"]
            self.FSIP.Function = fsMappingRule["Function"]
            self.FSIP.IP = "0.0.0.0"
            del self.FSIP.Nodes  # 不需要這個屬性
            self.jsonObj.FSIPs.append(self.FSIP)

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] ADDFSIP Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)
