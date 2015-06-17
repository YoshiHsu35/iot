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


class DecisionAction():

    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        if (spreate_obj_json_msg["Control"]=="REG"):
            print "Start subscriber TopicName: %s" % spreate_obj_json_msg["Gateway"]

            gwobj = class_Obj.GatewayObj(spreate_obj_json_msg["Gateway"])
            IoTServer._globalGWList.append(gwobj)
            for p in IoTServer._globalGWList: print("_globalGWList:"+gwobj.Name)


            class_MQTTManager.SubscriberThreading(spreate_obj_json_msg["Gateway"]).start()

        elif (spreate_obj_json_msg["Control"] == "ADDNODE"):
            for gwobj in IoTServer._globalGWList:
                if(gwobj.Name == spreate_obj_json_msg["Gateway"]):
                    print("yaaaaaaaaaa")


            # global _g_nodeList
            #
            # isSendNodeSuccess = False
            #
            # for node_client in _g_nodeList:
            #
            #     if(node_client[1]==spreate_obj_json_msg["Device"]):
            #         #轉成文字
            #         _str_sendToGWJson = json.dumps(spreate_obj_json_msg)
            #         print "Ready to transport message is: %s" % _str_sendToGWJson
            #
            #         try:
            #             node_client[0].send(_str_sendToGWJson)
            #             isSendNodeSuccess = True
            #         except:
            #             print "[ERROR] send to node have some error!"
            #             isSendNodeSuccess = False
            #
            # if not isSendNodeSuccess:
            #     print "Destination Node:%s didn't online" % spreate_obj_json_msg["Device"]

        else:
            print "[INFO] Receive message in wrong GW name!"

