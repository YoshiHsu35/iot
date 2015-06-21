#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_MQTTManager
import class_Obj
import thread
import M2MFunctionServer
import M2MRule


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control REQTOPICLIST ##########

        if (spreate_obj_json_msg["Control"] == "REQTOPICLIST"):
            print "[DecisionActions] REQTOPICLIST TopicName: %s" % spreate_obj_json_msg["Gateway"]

            m2mfsmrules = M2MRule.FunctionServerMappingRules()

            m2mfsmrules.replyM2MTopicToGW("FS1",spreate_obj_json_msg["Gateway"])


        elif (spreate_obj_json_msg["Control"] == "GETRULE"):
            m2mfsmrules = M2MRule.FunctionServerMappingRules()

            m2mfsmrules.replyM2MRulesAll("FS1")


        # elif (spreate_obj_json_msg["Control"] == "ADDRULE"):
        #
        #
        # elif (spreate_obj_json_msg["Control"] == "UPDATERULE"):
        #
        #
        # elif (spreate_obj_json_msg["Control"] == "DELRULE"):


        else:
            print "[DecisionActions] Receive message in wrong Control Signal! json:%s" %(spreate_obj_json_msg)


