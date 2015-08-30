#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

from Rules import *


class DecisionAction():
    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control GWREG ##########

        if (spreate_obj_json_msg["Control"] == "GWREG"):
            print("[DecisionActions] Start subscriber TopicName: %s" % spreate_obj_json_msg["Gateway"])

            ## 防止重複註冊
            IsAlreadyREG = False

            for p in IoTServer._globalGWList:
                if (p.Name == spreate_obj_json_msg["Gateway"]): IsAlreadyREG = True

            if (not IsAlreadyREG):

                gwobj = GatewayObj(spreate_obj_json_msg["Gateway"])
                IoTServer._globalGWList.append(gwobj)

                tempprint = "[DecisionActions] REG GW From %s ,_globalGWList:" % (gwobj.Name)
                for p in IoTServer._globalGWList: tempprint += p.Name + ", "

                print(tempprint)

                SubscriberThreading(spreate_obj_json_msg["Gateway"]).start()

            else:
                print("[DecisionActions] REG GW Fail!, due to this GW already REG!")

        ########## Control ADDNODE ##########

        elif (spreate_obj_json_msg["Control"] == "ADDNODE"):
            print("[DecisionActions] Start AddNode")
            IsAddNode = False
            for gwobj in IoTServer._globalGWList:
                # print("Current GWOBJ: "+ str(gwobj) + " name:"+ str(gwobj.Name))
                if (gwobj.Name == spreate_obj_json_msg["Gateway"]):
                    # print("in Current GWOBJ: "+ str(gwobj) + " name:"+ str(gwobj.Name))

                    for node in spreate_obj_json_msg["Nodes"]:
                        nodeobj = NodeObj(node["Node"], node["NodeFunction"], node["Functions"])
                        # print("in nodeobj "+str(nodeobj))
                        gwobj.Nodes.append(nodeobj)
                        print("[DecisionActions] ADDNODE From %s, NodeName is %s, NodeFunction is %s, Functions is %s" %
                              (gwobj.Name, node["Node"], node["NodeFunction"], node["Functions"]))

                        # for g in gwobj.Nodes:
                        #    print(g.Functions)

                    IsAddNode = True

                    fsmapping = FunctionServerMappingRules()
                    fsmapping.replyFSTopicToGW(spreate_obj_json_msg["Gateway"], gwobj.Nodes)

            if (not IsAddNode):
                print("[DecisionActions] ADDNODE Not found specific GW.")

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
                                print("[DecisionActions] DELNODE remove %s" % (nodes.Name))
                                gwobj.Nodes.remove(nodes)
                                IsDelNode = True
                        except:
                            pass

            if (not IsDelNode):
                print("[DecisionActions] DELNODE Not found specific GW.")

        ############### Manage Device ###############
        #############################################
        ########## Control MANAGEDEVICEREG ##########
        #############################################

        elif (spreate_obj_json_msg["Control"] == "MANAGEDEVICEREG"):
            print("[DecisionActions] Start subscriber TopicName: %s" % spreate_obj_json_msg["Device"])

            ## 防止重複註冊
            IsAlreadyREG = False

            for p in IoTServer._globalMANAGEDEVICEList:
                if (p.Name == spreate_obj_json_msg["Device"]): IsAlreadyREG = True

            if (not IsAlreadyREG):

                manObj = ManageObj(spreate_obj_json_msg["Device"])
                IoTServer._globalMANAGEDEVICEList.append(manObj)

                tempprint = "[DecisionActions] REG MANAGEDEVICE From %s ,_globalMANAGEDEVICEList:" % (manObj.Name)
                for p in IoTServer._globalMANAGEDEVICEList: tempprint += p.Name + ", "

                print(tempprint)

                SubscriberThreading(spreate_obj_json_msg["Device"]).start()

            else:
                print("[DecisionActions] REG MANAGEDEVICE Fail!, due to this MANAGEDEVICE already REG!")

        ########## Control DEVICEREQFS ##########
        elif (spreate_obj_json_msg["Control"] == "DEVICEREQFS"):
            fsmapping = FunctionServerMappingRules()
            fsmapping.replyFSTopicToMANAGEDEV(spreate_obj_json_msg["Device"])

        else:
            print("[DecisionActions] Receive message in wrong Control Signal! json:%s" % (spreate_obj_json_msg))
