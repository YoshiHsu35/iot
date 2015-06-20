#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_MQTTManager
import class_Obj
import IoTServer
import Rules
import thread


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control REQTOPICLIST ##########

        if (spreate_obj_json_msg["Control"] == "REQTOPICLIST"):


            ## TODO 補上REQTOPIC
            A = 1


        else:
            print "[DecisionActions] Receive message in wrong Control Signal! json:%s" %(spreate_obj_json_msg)


