#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Nathaniel'
import json


###############################################################

class JSON_REPTOPICLIST():
    ###因為是自訂類別，所以要用這種方式轉出
    ## http://stackoverflow.com/questions/3768895/python-how-to-make-a-class-json-serializable
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

    def __init__(self):
        self.Gateway = ""
        self.Control = "REPTOPICLIST"
        self.SubscribeTopics = []  # SubscribeTopicsObj


class SubscribeTopicsObj:
    def __init__(self):
        self.TopicName = ""
        self.Node = ""
        self.Target = ""
        self.Value = ""


###############################################################

class JSON_M2MRULE():
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

    def __init__(self):
        self.Control = "REPRULE"
        self.Rules = []


class RuleObj:
    def __init__(self):
        self.RuleID = ""
        self.InputGW = ""
        self.InputNode = ""
        self.InputIO = ""
        self.OutputGW = ""
        self.OutputNode = ""
        self.OutputIO = ""
        self.OutputValue = ""
