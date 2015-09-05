#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_M2MFS_MQTTManager
import class_M2MFS_Obj
import M2MFunctionServer
from M2MRule import *
from terminalColor import bcolors


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control REQTOPICLIST ##########

        if (spreate_obj_json_msg["Control"] == "REQTOPICLIST"):
            print(bcolors.OKBLUE + "[DecisionActions] REQTOPICLIST TopicName: %s" % spreate_obj_json_msg[
                "Gateway"] + bcolors.ENDC)

            m2mfsmrules = FunctionServerMappingRules()

            m2mfsmrules.replyM2MTopicToGW("FS1", spreate_obj_json_msg["Gateway"])


        elif (spreate_obj_json_msg["Control"] == "GETRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.replyM2MRulesAll("FS1")

        elif (spreate_obj_json_msg["Control"] == "ADDRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.AddM2MRule(spreate_obj_json_msg["Rules"])

        elif (spreate_obj_json_msg["Control"] == "UPDATERULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.UpdateM2MRule(spreate_obj_json_msg["Rules"])

        elif (spreate_obj_json_msg["Control"] == "DELRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.DelM2MRule(spreate_obj_json_msg["Rules"])

        else:
            print(bcolors.FAIL + "[DecisionActions] Receive message in wrong Control Signal! json:%s" % (
            spreate_obj_json_msg) + bcolors.ENDC)
