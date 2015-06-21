#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_Obj
import class_MQTTManager
import json


# RuleID, Input GW, Input Node, Input IO, Output GW, Output Node, Output IO, Output Value
_g_M2MRulesMappingList = [["1", "GW1", "N1", "SW1", "GW2", "N2", "LED3", "DEF"],
                          ["2", "GW1", "N1", "SW1", "GW2", "N2", "LED4", "0"],
                          ["3", "GW2", "N2", "SW2", "GW1", "N1", "LED2", "1"]]


class FunctionServerMappingRules():
    def __init__(self):
        self.jsonObj = class_Obj.JSON_REPTOPICLIST()

    def replyM2MTopicToGW(self, topicName, GWName):
        self.jsonObj.Gateway = GWName
        IsGWHaveM2MMappingRules = False
        readyToReplyTopics = []

        for SingleM2MMappingRule in _g_M2MRulesMappingList:

            if (SingleM2MMappingRule[4] == GWName):
                readyToReplyTopics.append(SingleM2MMappingRule)

        if (len(readyToReplyTopics) > 0):
            IsGWHaveM2MMappingRules = True
            for SingleM2MMappingRule in readyToReplyTopics:
                #### ASSIGN TO M2M FS ####
                self.SubscribeTopics = class_Obj.SubscribeTopicsObj()
                self.SubscribeTopics.TopicName = str(SingleM2MMappingRule[1]) + "/" + str(
                    SingleM2MMappingRule[2]) + "/" + SingleM2MMappingRule[3]  # FS1
                self.SubscribeTopics.Node = SingleM2MMappingRule[5]  # M2M
                self.SubscribeTopics.Target = SingleM2MMappingRule[6]
                self.SubscribeTopics.Value = SingleM2MMappingRule[7]

                self.jsonObj.SubscribeTopics.append(self.SubscribeTopics)

        else:
            IsGWHaveM2MMappingRules = False

        jsonstring = self.jsonObj.to_JSON()

        print("[Rules] REPTOPICLIST Send to topic:%s" % (topicName))

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyM2MRulesAll(self, topicName):
        self.jsonObj = class_Obj.JSON_M2MRULE()

        for SingleM2MMappingRule in _g_M2MRulesMappingList:
            self.Rule = class_Obj.RuleObj()
            self.Rule.RuleID = SingleM2MMappingRule[0]
            self.Rule.InputGW = SingleM2MMappingRule[1]
            self.Rule.InputNode = SingleM2MMappingRule[2]
            self.Rule.InputIO = SingleM2MMappingRule[3]
            self.Rule.OutputGW = SingleM2MMappingRule[4]
            self.Rule.OutputNode = SingleM2MMappingRule[5]
            self.Rule.OutputIO = SingleM2MMappingRule[6]
            self.Rule.OutputValue = SingleM2MMappingRule[7]
            self.jsonObj.Rules.append(self.Rule)

        jsonstring = self.jsonObj.to_JSON()

        print("[Rules] REPRULE Send to topic:%s" % (topicName))

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)
