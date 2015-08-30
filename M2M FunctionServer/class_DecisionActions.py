#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
from class_MQTTManager import *
from class_Obj import *
from M2MFunctionServer import *
from M2MRule import *


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control REQTOPICLIST ##########

        if (spreate_obj_json_msg["Control"] == "REQTOPICLIST"):
            print("[DecisionActions] REQTOPICLIST TopicName: %s" % spreate_obj_json_msg["Gateway"])

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
            print("[DecisionActions] Receive message in wrong Control Signal! json:%s" % (spreate_obj_json_msg))
