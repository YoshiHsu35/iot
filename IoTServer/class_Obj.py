#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Nathaniel'
import json

###############################################################

class NodeObj():
    def __init__(self, NodeName, NodeFunction, Functions):
        self.Name = NodeName
        self.NodeFunction = NodeFunction
        self.Functions = Functions


class GatewayObj():
    def __init__(self, GWName):
        self.Name = GWName
        self.Nodes = [] #放NodeObj

###############################################################

class ManageObj():
    def __init__(self, MANAGEName):
        self.Name = MANAGEName


###############################################################

class JSON_ADDFSIP():

    ###因為是自訂類別，所以要用這種方式轉出
    ## http://stackoverflow.com/questions/3768895/python-how-to-make-a-class-json-serializable
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)#, indent=4) 要indent在uncommit

    def __init__(self):
        self.Control="ADDFSIP"
        self.FSIPs = [] #放FSIPObj

class FSIPObj:
    def __init__(self):
        self.FunctionTopic=""
        self.Function=""
        self.IP = "0.0.0.0"
        self.Nodes = [] #放Node名稱就好(純字串)

###############################################################
