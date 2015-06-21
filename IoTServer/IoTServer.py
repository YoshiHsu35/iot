#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import json
import copy
import sys

import class_MQTTManager



#上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


_globalGWList = []
_globalMANAGEDEVICEList = []

print("::::::::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::::::::")
print("'####::'#######::'########::'######::'##::::'##:")
print(". ##::'##.... ##:... ##..::'##... ##: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##:::: ##:::..:: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##::::. ######:: ##:::: ##:")
print(": ##:: ##:::: ##:::: ##:::::..... ##:. ##:: ##::")
print(": ##:: ##:::: ##:::: ##::::'##::: ##::. ## ##:::")
print("'####:. #######::::: ##::::. ######::::. ###::::")
print("....:::.......::::::..::::::......::::::...:::::")
print("::::::::::::::::::::::::::::::::::::::::::::::::\n")


def main():
    class_MQTTManager.SubscriberThreading("IOTSV/REG").start()

    #sm = class_MQTTManager.SubscriberManager()
    #sm.subscribe("GW1")

if __name__ == '__main__':
        main()

