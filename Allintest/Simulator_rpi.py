#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json
import blescan

import bluetooth._bluetooth as bluez

import NIT_Node_Module
from terminalColor import bcolors

NodeUUID = "NODE-RPi-CUTE-ANIMALS"
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["LED1", "LED2", "SW1"]
NodeFunctions = ['IOs', 'IPCams']

print("::::::::::::::::::::::::::::::::::::::::::\n")
print("::::::::::::::::::::::::::::::::::::::::::\n")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")

nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions)


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
    # print("thread name：　" + threading.current_thread().getName())

    # callback
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        nit.RegisterNoode()

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):
    nit.M2M_RxRouting(_obj_json_msg)


global flip
def loop():
    global flip
    decide = "g"
    decide = input("enter 't' to trigger")
    print(decide)

    initMSGObj = {'TopicName': "NODE-01/SW1", 'Control': 'M2M_SET', 'Source': "NODE-01", 'M2M_Value': flip}
    initMSGSTR = json.dumps(initMSGObj)

    if (decide == "t"):
        nit.DirectMSG("NODE-01/SW1", initMSGSTR)
        print("SW01 SENT.")
        flip = (~flip)

    

#SCAN BLE LOOP
def scanloop():

    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        #print("ble thread started")

    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    while True:

        global beacon
        beacon = ''
        #if(beacon==''):
            #initMSGObj = {'TheKidLoc': "CHILD_DISAPPEAR", 'Control': 'BLE_SCAN', 'Source': "NODE-RPi", 'BLEUUID': beacon[18:50]}
            #initMSGSTR = json.dumps(initMSGObj)
    
            #nit.DirectMSG(beacon[18:50]+"/NODE-RPi", initMSGSTR)
            #time.sleep(1)


        
        returnedList = blescan.parse_events(sock, 1)
        #print("----------")
        for beacon in returnedList:
            #print(beacon[18:50])
            pass
            
        #'TopicName': "fda50693a4e24fb1afcfc6eb07647825/NODE-RPi"
        
        if(beacon!=''):
            initMSGObj = {'TheKidLoc': NodeUUID, 'Control': 'BLE_SCAN', 'Source': "NODE-RPi", 'BLEUUID': beacon[18:50]}
            initMSGSTR = json.dumps(initMSGObj)
            #print("test--test--test")

            nit.DirectMSG(beacon[18:50]+"/NODE-RPi", initMSGSTR)

            time.sleep(1)

        

if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    MQTT_Thread.join()
    #global flip
    #flip = 0
    while True:
        scanloop()
