#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import socket
import sys
import time
import json
import copy
import signal
import sys

#_g_cst_gatewayName = "GW2"
_g_cst_gatewayName = "GW1"

_g_cst_ToServerSocketIP = "127.0.0.1"
#_g_cst_ToServerSocketIP = "192.168.1.31"

_g_cst_GWSocketServerPort = 50005

_g_cst_NodeToGWSocketIP = ''  # 不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_NodeToGWSocketPort = 50000
_g_cst_MaxNodeConnectionCount = 10
_g_cst_NodeConnectionTimeOut = 1000

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
                    print("[ERROR] Server Socket error, disconnected this socket. Error Message:%s" % message)
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
    global _g_nodeList

    for node_client in _g_nodeList:

        if(node_client[1]==spreate_obj_json_msg["Device"]):
            #轉成文字
            _str_sendToGWJson = json.dumps(spreate_obj_json_msg)
            print "Ready to transport message is: %s" % _str_sendToGWJson
            
            try:
                node_client[0].send(_str_sendToGWJson)
            except:
                print "[ERROR] send to node have some error!"
        else:
            print "Destination Node:%s didn't online" % spreate_obj_json_msg["Device"]



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


            _str_recvMsg = client.recv(1024)
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
                    #將此GW加入GW清單中
                    _g_nodeList.append(nodeInfo)
                    print ("[REGISTE] Node %s" % nodeInfo)
                    ClientRegisted = True

            except:
                ClientRegisted = False
                print("[ERROR] No Server connected yet!")



    try:
        GWServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.stderr.write("[ERROR] Failed create Node listen socket! %s\n" % msg[1])
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

