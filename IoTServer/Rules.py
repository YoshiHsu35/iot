#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_Obj
import class_MQTTManager
import json

_g_FunctionServerMappingList = [["FS1", "M2M","IOs"],["FS2", "Streaming", "IPCams"]]  #看到NodeFunction名為IOs的，代表該Node的訊息要Mapping到M2M的FS，他的TOPIC為FS1

class FunctionServerMappingRules():

    def __init__(self):
        self.jsonObj = class_Obj.JSON_ADDFSIP()


    def replyFSTopicToGW(self, topicName, GWObj):
        self.jsonObj.Control = "ADDFSIP"
        for fsMappingRule in _g_FunctionServerMappingList:

            IsFSHaveNodeMapping = False

            #### ASSIGN TO M2M FS ####
            self.FSIP = class_Obj.FSIPObj()
            self.FSIP.FunctionTopic=fsMappingRule[0] #FS1
            self.FSIP.Function=fsMappingRule[1] #M2M
            self.FSIP.IP = "0.0.0.0"
            self.FSIP.Nodes = []

            for nodeObj in GWObj:

                if(nodeObj.NodeFunction == fsMappingRule[2]): #IOs
                    self.FSIP.Nodes.append(nodeObj.Name)
                    IsFSHaveNodeMapping = True

            #如果規則中的function在GW下面的Node找不到，則不需要回傳該function所要的topic
            if(IsFSHaveNodeMapping):
                self.jsonObj.FSIPs.append(self.FSIP)


        jsonstring = self.jsonObj.to_JSON()

        print("[Rules] ADDFSIP Send to topic:%s" %(topicName))

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName,jsonstring)

    def replyFSTopicToMANAGEDEV(self, topicName):

        for fsMappingRule in _g_FunctionServerMappingList:

            IsFSHaveNodeMapping = False

            #### ASSIGN TO M2M FS ####
            self.FSIP = class_Obj.FSIPObj()
            self.FSIP.FunctionTopic=fsMappingRule[0]
            self.FSIP.Function=fsMappingRule[1]
            self.FSIP.IP = "0.0.0.0"
            del self.FSIP.Nodes #不需要這個屬性
            self.jsonObj.FSIPs.append(self.FSIP)


        jsonstring = self.jsonObj.to_JSON()

        print("[Rules] ADDFSIP Send to topic:%s" %(topicName))

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName,jsonstring)