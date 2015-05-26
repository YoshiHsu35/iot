﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import socket
from gevent import Timeout
import time
import json
import copy
import sys
import paho.mqtt.client as mqtt

#_g_cst_gatewayName = "GW2"
_g_cst_gatewayName = "GW1"


_g_cst_ToServerSocketIP = "127.0.0.1"
#_g_cst_ToServerSocketIP = "122.117.119.197"

_g_cst_GWSocketServerPort = 50005

_g_cst_NodeToGWSocketIP = ''  # 不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_NodeToGWSocketPort = 50000
_g_cst_MaxNodeConnectionCount = 10
_g_cst_NodeConnectionTimeOut = 1000  # non-blocking寫法，目前無用，不要un-commit這個數值所使用的程式碼段落

_g_cst_socketClientTimeout = 120  # 如果在指定的秒數之內，gw都沒有訊息，視為time out 120 second

_g_cst_ToMQTTTopicServerIP = "thkaw.no-ip.biz"
_g_cst_ToMQTTTopicServerPort = "1883"

_g_cst_MQTTTopicName = "NCKU/NEAT/TOPIC/01"


_g_cst_ToGWProtocalHaveMQTT = True
#_g_cst_ToGWProtocalHaveSocket = True #Default enable, can't disable for now


print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":'######::::::'###::::'########:'########:'##:::::'##::::'###::::'##:::'##:")
print("'##... ##::::'## ##:::... ##..:: ##.....:: ##:'##: ##:::'## ##:::. ##:'##::")
print(" ##:::..::::'##:. ##::::: ##:::: ##::::::: ##: ##: ##::'##:. ##:::. ####:::")
print(" ##::'####:'##:::. ##:::: ##:::: ######::: ##: ##: ##:'##:::. ##:::. ##::::")
print(" ##::: ##:: #########:::: ##:::: ##...:::: ##: ##: ##: #########:::: ##::::")
print(" ##::: ##:: ##.... ##:::: ##:::: ##::::::: ##: ##: ##: ##.... ##:::: ##::::")
print(". ######::: ##:::: ##:::: ##:::: ########:. ###. ###:: ##:::: ##:::: ##::::")
print(":......::::..:::::..:::::..:::::........:::...::...:::..:::::..:::::..:::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")


########### Normal Socket to Server(As socket client) ##############

_g_serverList = []


def GatewayToServerSocketThread():
    devicePollingInterval = 1
    _b_isEstablishedConnect = False

    while(True):

        while (not _b_isEstablishedConnect):
            try:
                ToServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                sys.stderr.write("[ERROR] %s\n" % msg[1])
                sys.exit(1)

            try:
                ToServerSocket.connect((_g_cst_ToServerSocketIP, _g_cst_GWSocketServerPort))

                # 若與server連線建立成功，把這個連線存到server list，讓其他的部分可以調用傳訊息上Server
                _g_serverList.append(ToServerSocket)
                _b_isEstablishedConnect = True
                print('===============================================\n')
                print('---------------Gateway(%s)->>>Server---------------\n' % _g_cst_gatewayName)
                print('>>>Start connect Server %s<<<' % (time.asctime(time.localtime(time.time()))))
                print('===============================================\n')


                # 向Server註冊
                print("[INFO] Connecting Server successful!\n")
                ToServerSocket.send('{"Gateway":"%s","Control":"REG"}' % (_g_cst_gatewayName))

            except socket.error, msg:
                print("[ERROR] Failed connecting to Server! %s\n" % msg[1])
                #exit(1)


        while (_b_isEstablishedConnect):
                time.sleep(devicePollingInterval)

                try:
                    _str_recvMsg = ToServerSocket.recv(256)

                except socket.error, (value, message):
                    print("[ERROR] Server Socket error, disconnected this Server. Error Message:%s" % message)
                    ToServerSocket.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                    ToServerSocket.close()
                    _g_serverList.remove(ToServerSocket)
                    _b_isEstablishedConnect = False
                    break


                _str_decodeMsg = _str_recvMsg.decode('utf-8')

                print("[MESSAGE] Reciving message from [Server] at %s : \n >>> %s <<<" % (
                    time.asctime(time.localtime(time.time())), _str_recvMsg))

                try:
                    _obj_json_msg = json.loads(_str_recvMsg)

                except:
                    print("[ERROR] Couldn't converte json to Objet!")

                RoutingNode(_obj_json_msg)


def RoutingNode(_obj_json_msg):
    spreate_obj_json_msg = copy.copy(_obj_json_msg)
    if (spreate_obj_json_msg["Gateway"]==_g_cst_gatewayName):
        global _g_nodeList

        isSendNodeSuccess = False

        for node_client in _g_nodeList:

            if(node_client[1]==spreate_obj_json_msg["Device"]):
                #轉成文字
                _str_sendToGWJson = json.dumps(spreate_obj_json_msg)
                print "Ready to transport message is: %s" % _str_sendToGWJson

                try:
                    node_client[0].send(_str_sendToGWJson)
                    isSendNodeSuccess = True
                except:
                    print "[ERROR] send to node have some error!"
                    isSendNodeSuccess = False

        if not isSendNodeSuccess:
            print "Destination Node:%s didn't online" % spreate_obj_json_msg["Device"]

    else:
        print "[INFO] Receive message in wrong GW name!"


t_GatewayServer = Thread(target=GatewayToServerSocketThread, args=())
t_GatewayServer.start()


########### Normal Socket to Nodes(As socket Server) ##############

_g_nodeList = []


def NodeToGatewaySocketThread():
    devicePollingInterval = 1

    def clientServiceThread(client):

        # 若node連線建立成功，把這個連線存到node list，讓其他的部分可以調用傳訊息

        nodeInfo = []
        nodeInfo.append(client)

        ClientRegisted = False

        while (True):
            time.sleep(devicePollingInterval)

            _str_recvMsg = None

            with Timeout(_g_cst_socketClientTimeout, False):
                try:
                    _str_recvMsg = client.recv(1024)

                except socket.error, (value,message):
                    print("[ERROR] Socket error, disconnected this node. Error Message:%s" % message)
                    client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                    client.close()
                    for nodeinfo in _g_nodeList:
                        if nodeinfo[1] == _obj_json_msg["Device"]:
                            print ("[INFO] Remove Device: %s" % nodeinfo[1])
                            _g_nodeList.remove(nodeinfo)
                    return


                _str_decodeMsg = _str_recvMsg.decode('utf-8')


                print("[MESSAGE] Reciving message from [Node] at %s : \n >>> %s <<<" % (
                    time.asctime(time.localtime(time.time())), _str_recvMsg))


                try:
                    #將文字轉成object
                    _obj_json_msg = json.loads(_str_recvMsg)

                    #插入新的attribute
                    _obj_json_msg["Gateway"] = _g_cst_gatewayName

                    #轉成文字
                    _str_sendToSvJson = json.dumps(_obj_json_msg)


                except:
                    print("[ERROR] Couldn't converte json to Objet!")

                try:
                    #從ServerList裡面挑第一個Server送Json字串上去
                    _g_serverList[0].send(_str_sendToSvJson)

                    #成功後再註冊DEVICE
                    if not ClientRegisted:
                        nodeInfo.append(_obj_json_msg["Device"])
                        #將此Node加入Node清單中
                        _g_nodeList.append(nodeInfo)
                        print ("[REGISTE] Node %s" % nodeInfo)
                        ClientRegisted = True

                except:
                    ClientRegisted = False
                    print("[ERROR] No Server connected yet!")

            if _str_recvMsg is None:
                client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                client.close()
                print("[ERROR] Socket timeout, disconnected this node.")
                for nodeinfo in _g_nodeList:
                    if nodeinfo[1] == _obj_json_msg["Device"]:
                        print ("[INFO] Remove Device: %s" % nodeinfo[1])
                        _g_nodeList.remove(nodeinfo)
                return

    try:
        GWServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print("[ERROR] Failed create Node listen socket! %s\n" % msg[1])
        sys.exit(1)

    GWServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse tcp
    GWServerSocket.bind((_g_cst_NodeToGWSocketIP, _g_cst_NodeToGWSocketPort))
    GWServerSocket.listen(_g_cst_MaxNodeConnectionCount)
    # GWServerSocket.settimeout(_g_cst_NodeConnectionTimeOut)

    print('===============================================')
    print('----------------Node->>>Gateway----------------\n')
    print('>>>Start listen Devices %s<<<' % (time.asctime(time.localtime(time.time()))))
    print('===============================================\n')

    while True:
        (clientSocket, address) = GWServerSocket.accept()
        print("[INFO] Client Info: ", clientSocket, address)
        t = Thread(target=clientServiceThread, args=(clientSocket,))
        t.start()


t_NodeGateway = Thread(target=NodeToGatewaySocketThread, args=())
t_NodeGateway.start()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("[INFO] Connected MQTT Topic Server:"+ _g_cst_MQTTTopicName +" with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(_g_cst_MQTTTopicName)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("[INFO] MQTT message receive from Topic %s at %s :%s" %(msg.topic,time.asctime(time.localtime(time.time())), str(msg.payload)))

    try:
        _obj_json_msg = json.loads(msg.payload)
        RoutingNode(_obj_json_msg)
    except:
        print("[ERROR] Couldn't converte json to Objet!")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()