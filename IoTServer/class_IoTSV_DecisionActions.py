#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_IoTSV_MQTTManager
import class_IoTSV_Obj
import IoTServer
import Rules
from terminalColor import bcolors


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)


        ########## Control GWREG ##########

        if (spreate_obj_json_msg["Control"] == "GWREG"):
            print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
                  spreate_obj_json_msg["Gateway"] + bcolors.ENDC)

            ## 防止重複註冊
            IsAlreadyREG = False

            for p in IoTServer._globalGWList:
                if (p.Name == spreate_obj_json_msg["Gateway"]): IsAlreadyREG = True

            if (not IsAlreadyREG):

                gwobj = class_IoTSV_Obj.GatewayObj(spreate_obj_json_msg["Gateway"])
                IoTServer._globalGWList.append(gwobj)

                tempprint = "[DecisionActions] REG GW From %s ,_globalGWList:" % (gwobj.Name)
                for p in IoTServer._globalGWList: tempprint += p.Name + ", "

                print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                class_IoTSV_MQTTManager.SubscriberThreading(spreate_obj_json_msg["Gateway"]).start()

            else:
                print(bcolors.FAIL + "[DecisionActions] REG GW Fail!, due to this GW already REG!" + bcolors.ENDC)


        ########## Control FSREG ##########
        elif (spreate_obj_json_msg["Control"] == "FSREG"):
            print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
                  spreate_obj_json_msg["FunctionServer"] + bcolors.ENDC)

            ## 防止重複註冊
            FSIsAlreadyREG = False

            for p in IoTServer._globalFSList:
                if (p.Name == spreate_obj_json_msg["FunctionServer"]): FSIsAlreadyREG = True

            if (not FSIsAlreadyREG):

                fsobj = class_IoTSV_Obj.FunctionServerObj(spreate_obj_json_msg["FunctionServer"])
                fsobj.Function = spreate_obj_json_msg["Function"]
                IoTServer._globalFSList.append(fsobj)

                tempprint = "[DecisionActions] REG fs From %s ,_globalFSList:" % (fsobj.Name)
                for p in IoTServer._globalFSList: tempprint += p.Name + ", "

                print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                #class_MQTTManager.SubscriberThreading(spreate_obj_json_msg["FunctionServer"]).start()

            else:
                print(bcolors.FAIL + "[DecisionActions] REG FS Fail!, due to this FS already REG!" + bcolors.ENDC)


        ########## Control ADDNODE ##########

        elif (spreate_obj_json_msg["Control"] == "ADDNODE"):
            print(bcolors.OKBLUE + "[DecisionActions] Start AddNode" + bcolors.ENDC)
            IsAddNode = False
            for gwobj in IoTServer._globalGWList:
                # print("Current GWOBJ: "+ str(gwobj) + " name:"+ str(gwobj.Name))
                if (gwobj.Name == spreate_obj_json_msg["Gateway"]):
                    # print("in Current GWOBJ: "+ str(gwobj) + " name:"+ str(gwobj.Name))

                    for node in spreate_obj_json_msg["Nodes"]:
                        nodeobj = class_IoTSV_Obj.NodeObj(node["Node"], node["NodeFunction"], node["Functions"])
                        # print("in nodeobj "+str(nodeobj))
                        gwobj.Nodes.append(nodeobj)
                        print(
                            bcolors.OKGREEN + "[DecisionActions] ADDNODE From %s, NodeName is %s, NodeFunction is %s, Functions is %s" %
                            (gwobj.Name, node["Node"], node["NodeFunction"], node["Functions"]) + bcolors.ENDC)

                        # for g in gwobj.Nodes:
                        #    print(g.Functions)

                    IsAddNode = True

                    fsmapping = Rules.FunctionServerMappingRules()
                    fsmapping.replyFSTopicToGW(spreate_obj_json_msg["Gateway"], gwobj.Nodes)

            if (not IsAddNode):
                print(bcolors.FAIL + "[DecisionActions] ADDNODE Not found specific GW." + bcolors.ENDC)

        ########## Control DELNODE ##########

        elif (spreate_obj_json_msg["Control"] == "DELNODE"):
            IsDelNode = False
            jsonTempObj_Nodes = spreate_obj_json_msg["Nodes"]
            for gwobj in IoTServer._globalGWList:
                if (gwobj.Name == spreate_obj_json_msg["Gateway"]):
                    for nodes in gwobj.Nodes:

                        try:
                            searchIndex = jsonTempObj_Nodes.index(nodes.Name)
                            if (searchIndex > -1):
                                print(bcolors.OKGREEN + "[DecisionActions] DELNODE remove %s" % (
                                    nodes.Name) + bcolors.ENDC)
                                gwobj.Nodes.remove(nodes)
                                IsDelNode = True
                        except:
                            pass

            if (not IsDelNode):
                print(bcolors.FAIL + "[DecisionActions] DELNODE Not found specific GW." + bcolors.ENDC)

        ############### Manage Device ###############
        #############################################
        ########## Control MANAGEDEVICEREG ##########
        #############################################

        elif (spreate_obj_json_msg["Control"] == "MANAGEDEVICEREG"):
            print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
                  spreate_obj_json_msg["Device"] + bcolors.ENDC)

            ## 防止重複註冊
            IsAlreadyREG = False

            for p in IoTServer._globalMANAGEDEVICEList:
                if (p.Name == spreate_obj_json_msg["Device"]): IsAlreadyREG = True

            if (not IsAlreadyREG):

                manObj = class_IoTSV_Obj.ManageObj(spreate_obj_json_msg["Device"])
                IoTServer._globalMANAGEDEVICEList.append(manObj)

                tempprint = "[DecisionActions] REG MANAGEDEVICE From %s ,_globalMANAGEDEVICEList:" % (manObj.Name)
                for p in IoTServer._globalMANAGEDEVICEList: tempprint += p.Name + ", "

                print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                class_IoTSV_MQTTManager.SubscriberThreading(spreate_obj_json_msg["Device"]).start()

            else:
                print(
                    bcolors.FAIL + "[DecisionActions] REG MANAGEDEVICE Fail!, due to this MANAGEDEVICE already REG!" + bcolors.FAIL)

        ########## Control DEVICEREQFS ##########
        elif (spreate_obj_json_msg["Control"] == "DEVICEREQFS"):
            fsmapping = Rules.FunctionServerMappingRules()
            fsmapping.replyFSTopicToMANAGEDEV(spreate_obj_json_msg["Device"])

        else:
            print(bcolors.FAIL + "[DecisionActions] Receive message in wrong Control Signal! json:%s" % (
                spreate_obj_json_msg) + bcolors.ENDC)
