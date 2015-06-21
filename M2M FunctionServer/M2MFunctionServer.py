#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import json
import copy
import sys

import class_MQTTManager


# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort

#_globalGWList = []

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
    class_MQTTManager.SubscriberThreading("FS1").start()


if __name__ == '__main__':
    main()
