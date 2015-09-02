#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_Obj
import class_MQTTManager
import json
import copy
from terminalColor import bcolors

# RuleID, InputGW, InputNode, InputIO, OutputGW, OutputNode, OutputIO, OutputValue
# _g_M2MRulesMappingList = [["1", "GW1", "N1", "SW1", "GW2", "N2", "LED3", "DEF"],
#                         ["2", "GW1", "N1", "SW1", "GW2", "N2", "LED4", "0"],
#                         ["3", "GW2", "N2", "SW2", "GW1", "N1", "LED2", "1"]]

_g_M2MRulesMappingList = [{"RuleID": "1", "InputGW": "GW1", "InputNode": "N1", "InputIO": "SW1",
                           "OutputGW": "GW2", "OutputNode": "N2", "OutputIO": "LED3", "OutputValue": "DEF"},

                          {"RuleID": "2", "InputGW": "GW1", "InputNode": "N1", "InputIO": "SW1",
                           "OutputGW": "GW2", "OutputNode": "N2", "OutputIO": "LED4", "OutputValue": "0"},

                          {"RuleID": "3", "InputGW": "GW2", "InputNode": "N2", "InputIO": "SW2",
                           "OutputGW": "GW1", "OutputNode": "N1", "OutputIO": "LED2", "OutputValue": "1"}]


class FunctionServerMappingRules():
    def __init__(self):
        self.jsonObj = class_Obj.JSON_REPTOPICLIST()

    def replyM2MTopicToGW(self, topicName, GWName):
        self.jsonObj.Gateway = GWName
        IsGWHaveM2MMappingRules = False
        readyToReplyTopics = []

        for SingleM2MMappingRule in _g_M2MRulesMappingList:

            if (SingleM2MMappingRule["OutputGW"] == GWName):
                readyToReplyTopics.append(SingleM2MMappingRule)

        if (len(readyToReplyTopics) > 0):
            IsGWHaveM2MMappingRules = True
            for SingleM2MMappingRule in readyToReplyTopics:
                #### ASSIGN TO M2M FS ####
                self.SubscribeTopics = class_Obj.SubscribeTopicsObj()
                self.SubscribeTopics.TopicName = str(SingleM2MMappingRule["InputGW"]) + "/" + str(
                    SingleM2MMappingRule["InputNode"]) + "/" + SingleM2MMappingRule["InputIO"]  # FS1
                self.SubscribeTopics.Node = SingleM2MMappingRule["OutputNode"]  # M2M
                self.SubscribeTopics.Target = SingleM2MMappingRule["OutputIO"]
                self.SubscribeTopics.Value = SingleM2MMappingRule["OutputValue"]

                self.jsonObj.SubscribeTopics.append(self.SubscribeTopics)

        else:
            IsGWHaveM2MMappingRules = False

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPTOPICLIST Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyM2MRulesAll(self, topicName):
        self.jsonObj = class_Obj.JSON_M2MRULE()

        for SingleM2MMappingRule in _g_M2MRulesMappingList:
            self.Rule = class_Obj.RuleObj()
            self.Rule.RuleID = SingleM2MMappingRule["RuleID"]
            self.Rule.InputGW = SingleM2MMappingRule["InputGW"]
            self.Rule.InputNode = SingleM2MMappingRule["InputNode"]
            self.Rule.InputIO = SingleM2MMappingRule["InputIO"]
            self.Rule.OutputGW = SingleM2MMappingRule["OutputGW"]
            self.Rule.OutputNode = SingleM2MMappingRule["OutputNode"]
            self.Rule.OutputIO = SingleM2MMappingRule["OutputIO"]
            self.Rule.OutputValue = SingleM2MMappingRule["OutputValue"]
            self.jsonObj.Rules.append(self.Rule)

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPRULE Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def AddM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] ADDRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyGWs = []

        for SingleM2MMappingRule in RuleObjs:
            NotifyGWs.append(SingleM2MMappingRule["OutputGW"])
            _g_M2MRulesMappingList.append(SingleM2MMappingRule)

        self.ModifyRePublishToGW(NotifyGWs)
        print(bcolors.OKGREEN + "[Rules] ADDRULE end!" + bcolors.ENDC)

    def UpdateM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] UPDATERULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyGWs = []

        for SingleM2MMappingRule in RuleObjs:
            for updateRule in _g_M2MRulesMappingList:
                if (updateRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    # 蠻怪的，陣列內dict變動，list內卻沒有跟著變??，只好砍掉重新加入
                    NotifyGWs.append(updateRule["OutputGW"])
                    _g_M2MRulesMappingList.remove(updateRule)
                    _g_M2MRulesMappingList.append(SingleM2MMappingRule.copy())
                    NotifyGWs.append(SingleM2MMappingRule["OutputGW"])

        self.ModifyRePublishToGW(NotifyGWs)
        print(bcolors.OKBLUE + "[Rules] UPDATERULE end!" + bcolors.ENDC)

    def DelM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] DELRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyGWs = []

        for SingleM2MMappingRule in RuleObjs:
            for delRule in _g_M2MRulesMappingList:
                if (delRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    NotifyGWs.append(delRule["OutputGW"])
                    _g_M2MRulesMappingList.remove(delRule)

        self.ModifyRePublishToGW(NotifyGWs)
        print(bcolors.OKGREEN + "[Rules] DELRULE end!" + bcolors.ENDC)

    def ModifyRePublishToGW(self, NotifyGWs):
        print(bcolors.OKBLUE + "[Rules] Republish New M2M Rules for relate GW." + bcolors.ENDC)
        NotifyGWs = list(set(NotifyGWs))
        for gws in NotifyGWs:
            self.replyM2MRulesAll(gws)
