#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import json
import copy
import sys

from class_MQTTManager import *


# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort

# _globalGWList = []

print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print("'##::::'##::'#######::'##::::'##::::'########::'######::'##::::'##:")
print(" ###::'###:'##.... ##: ###::'###:::: ##.....::'##... ##: ##:::: ##:")
print(" ####'####:..::::: ##: ####'####:::: ##::::::: ##:::..:: ##:::: ##:")
print(" ## ### ##::'#######:: ## ### ##:::: ######:::. ######:: ##:::: ##:")
print(" ##. #: ##:'##:::::::: ##. #: ##:::: ##...:::::..... ##:. ##:: ##::")
print(" ##:.:: ##: ##:::::::: ##:.:: ##:::: ##:::::::'##::: ##::. ## ##:::")
print(" ##:::: ##: #########: ##:::: ##:::: ##:::::::. ######::::. ###::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")


def main():
    SubscriberThreading("FS1").start()


if __name__ == '__main__':
    main()
