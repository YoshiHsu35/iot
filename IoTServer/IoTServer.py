#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import os
import json
import copy
import sys

# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from class_MQTTManager import *

# 上層目錄
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
    SubscriberThreading("IOTSV/REG").start()

    # sm = class_MQTTManager.SubscriberManager()
    # sm.subscribe("GW1")


if __name__ == '__main__':
    main()
