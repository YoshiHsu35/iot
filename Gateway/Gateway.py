#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
import socket
import time
import json
import copy
import sys
import Subscriber_action
import Publisher_action

_g_cst_gatewayName = "GW1"
#_g_cst_gatewayName = "GW2"

_g_cst_NodeToGWSocketIP = '' # 不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_NodeToGWSocketPort = 10000
_g_cst_MaxNodeConnectionCount = 10
_g_cst_socketClientTimeout = 120  # 如果在指定的秒數之內，gw都沒有訊息，視為time out 120 second

_g_cst_ToMQTTTopicBroker = "thkaw.no-ip.biz"#當前Broker設定位置
_g_cst_ToMQTTTopicServerPort = "1883"#預設Port

_g_cst_MQTTRegTopicName = "IOTSV/REG"#GW一開始要和IoT_Server註冊，故需要傳送信息至指定的MQTT Channel
_g_cst_MQTTAcTopicName = _g_cst_gatewayName
_g_cst_GoalTopic = ""
_g_cst_ToGWProtocalHaveMQTT = True
ReplyTopicList = False
#_g_cst_ToGWProtocalHaveSocket = True #Default enable, can't disable for now
_g_nodeList = []

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

#Connect to MQTT Server for communication
def GatewayToServerMQTTThread():

    _b_MQTTConnected=False
    global publisher
    publisher = Publisher_action.PublisherManager()
    try:
        print('===============================================\n')
        print('---------------Gateway(%s)--->>>Server in MQTT-\n' % _g_cst_gatewayName)
        print('>>>Start connect Server %s<<<' % (time.asctime(time.localtime(time.time()))))
        print('===============================================\n')
        print('Register to IoT Server successful! \n')
    except:
        sys.stderr.write("[ERROR] The MQTT connect is broken.\n")
        sys.exit(1)
    try:
        Publisher_action.publisher.MQTT_PublishMessage('{"Gateway": "%s","Control": "GWREG"}' % _g_cst_gatewayName,_g_cst_MQTTRegTopicName)
        Subscriber_action.SubscriberThreading(_g_cst_MQTTRegTopicName).start()

        _b_MQTTConnected = True
    except:
        print "[INFO]Register error."
        sys.exit(1)

NodeTopic_list = []#記錄Topic 的名稱，以利之後對照新進Node的表
Rule = []
Target = []
########### Normal Socket to Server(As socket client) ##############
def RoutingNode(_obj_json_msg):
    global publisher
    separation_obj_json_msg = copy.copy(_obj_json_msg)
    if separation_obj_json_msg["Control"] == "ADDFSIP" :#Recive control from IoT Server for Function Server Topic
        _g_cst_MQTTFSTopicName = "%s" % separation_obj_json_msg["FSIPs"][0]["FunctionTopic"]
        FS_function = separation_obj_json_msg["FSIPs"][0]["Function"]
        try:
            ReqToFS = {"Gateway": "%s"%_g_cst_gatewayName, "Control": "REQTOPICLIST"}
            Send_json = json.dumps(ReqToFS)
            Publisher_action.publisher.MQTT_PublishMessage(Send_json,str(_g_cst_MQTTFSTopicName))
            Subscriber_action.SubscriberThreading(str(_g_cst_MQTTFSTopicName)).start()
        except:
            print "[ERROR] Send Request for topic list error!"
            return

    if separation_obj_json_msg["Control"] == "REPTOPICLIST":#GW向FS要求配對相關功能的輸出口（或對應輸入口）時，FS相回傳對應的Topic和目標、功能及變數
        subList_temp = []
        try:
            if separation_obj_json_msg["Gateway"] == _g_cst_gatewayName:
                subList_temp = separation_obj_json_msg["SubscribeTopics"]
                NodeTopic_list.append(subList_temp) #Add to list of GW/N2/SW Topic list
                for i in NodeTopic_list:
                    for j in i:
                        print ("The Topic %s rule will be store." % str(j["TopicName"]))
                        Subscriber_action.SubscriberThreading(str(j["TopicName"])).start()#收到TopicName立即訂閱對應GW/Node上的Topic
        except:
            print "[ERROR] Reptopiclist fail. "
    if  separation_obj_json_msg["Control"] == "SET":#接收到指定GW送來的Control信息，並將這些信息送至Node上進行控制
        for i in NodeTopic_list:
            for j in i:
                if j["TopicName"] == separation_obj_json_msg["TopicName"]:
                    global _g_nodeList
                    for n in Rule:
                        if n["TargetTopic"] == separation_obj_json_msg["TargetTopic"]:
                            SendToNode = {"Target": "%s" % j["Target"]}
                            SendToNode["Component"] = n["OutputIO"]
                            SendToNode["Value"] = n["OutputValue"]
                            SendToNode["Control"] = "SET"
                            SendToNode_json = json.dumps(SendToNode)
                        for nodeinfo in _g_nodeList:
                            if nodeinfo[1] == n["OutputNode"]:
                                nodeinfo[0].send(SendToNode_json)#使用Socket傳送信息至Node上
    if  separation_obj_json_msg["Control"] == "REPRULE":
        for i in separation_obj_json_msg["Rules"]:
            separation_obj_json_msg["TargetTopic"] = i["InputGW"]+"/"+i["InputNode"]+"/"+i["InputIO"]
            Rule.append(i)
            Subscriber_action.SubscriberThreading.start(i["InputGW"]+"/"+i["InputNode"]+"/"+i["InputIO"])


def NodeToGatewaySocketThread():#接收來自Node的註冊信息，並將之傳至IoT Server上註冊，並等待分配至FS
    nodePollingInterval = 1
    global publisher
    Nodelist_check = False
    def clientServiceThread(client):
        # 若node連線建立成功，把這個連線存到node list，讓其他的部分可以調用以傳送訊息
        nodeInfo = []
        nodeInfo.append(client)#將Node信息加入List中
        ClientRegisted = False
        while (True):
            time.sleep(nodePollingInterval)#定時delay
            receFromNode_json = None
            try:
                receFromNode_json = client.recv(1024)
                receFromNode_str = json.loads(receFromNode_json)#將接收到的字串轉換並儲存

            except socket.error, (value,message):
                print("[ERROR] Socket error, disconnected this node. Error Message:%s" % message)#可能會連結不到，代表client方並沒有傳送資料
                client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                client.close()
                for nodeinfo in _g_nodeList:
                    if nodeinfo[1] == receFromNode_str["Node"]:#如果沒收到任何信息，則代表斷線。Socket會傳送故定的信息告知還在線上，若client完全沒收到則代表斷線
                        print ("[INFO] Remove Node: %s" % nodeinfo[1])
                        _g_nodeList.remove(nodeinfo)#從List中移除斷線的Node
                return

            #_receFromNode = receFromNode_json.decode('utf-8')
            print("[MESSAGE] Reciving message from [Node] at %s : \n >>> %s <<<" % (
                time.asctime(time.localtime(time.time())), receFromNode_json))
            if receFromNode_str["Control"] == "REG":
                try:
                    #新的Node開始註冊
                    SendToOther = {"Gateway": "%s"%_g_cst_gatewayName}
                    SendToOther["Control"] = "ADDNODE"
                    SendToOther["Nodes"] = [{
                        "Node": "%s" % receFromNode_str["Node"],
                        "NodeFunction": "%s" %receFromNode_str["NodeFunction"],
                        "Functions": receFromNode_str["Functions"]
                         }]
                    #壓縮成Json 封包
                    _str_sendToSvJson = json.dumps(SendToOther)
                except:
                    print("[ERROR] Couldn't converte json to Objet!")
                try:
                    #註冊Node to IoT Server
                    if not ClientRegisted:
                        nodeInfo.append(receFromNode_str["Node"])
                        #將此Node加入Node清單中
                        _g_nodeList.append(nodeInfo)
                        print "[REGISTE] Node %s" % nodeInfo
                        Publisher_action.publisher.MQTT_PublishMessage(_str_sendToSvJson,_g_cst_MQTTAcTopicName)#Register to IoT Server for New Node
                        try:
                            Subscriber_action.SubscriberThreading(_g_cst_MQTTAcTopicName).start()
                        except:
                            print "Create Thread fails"
                        ClientRegisted = True

                except:
                    ClientRegisted = False
                    print("[ERROR] Register to Server fail!!")
            if receFromNode_str["Control"]=="REP":#註冊完畢後，將有機會收到來自Node往外傳的信息，GW需要藉由MQTT將之傳到指定的Topic上
                for i in _g_nodeList:
                    if i[1] == receFromNode_str["Node"]:
                        Nodelist_check=True
                if Nodelist_check ==True:
                    for i in NodeTopic_list:
                        for j in i:
                            if j["Node"] == receFromNode_str["Node"]:
                                Target_topic = "%s"%(_g_cst_gatewayName+"/"+str(receFromNode_str["Node"])+"/"+str(receFromNode_str["Component"]))
                                print "The Target Topic"
                                print Target_topic
                                SendToNodeTopic = {"Control": "SET"}
                                SendToNodeTopic["TopicName"] = Target_topic
                                SendToNodeTopic["Value"] = str(receFromNode_str["Value"])
                                SendToNodeTopic_json = json.dumps(SendToNodeTopic)
                                print SendToNodeTopic_json
                                publisher.MQTT_PublishMessage(SendToNodeTopic_json,Target_topic)#傳送資料至指定的Topic上
                            else:
                                print "No Publish to other Node"


        if receFromNode_json is None:#如果完全都沒有收到信息，此處為重新連結
            client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
            client.close()
            print("[ERROR] Socket timeout, disconnected this node.")
            for nodeinfo in _g_nodeList:
                if nodeinfo[1] == receFromNode_str["Node"]:
                    print ("[INFO] Remove Node: %s" % nodeinfo[1])
                    remove_msg = ""
                    remove_msg["Gateway"]=_g_cst_gatewayName
                    remove_msg["Control"]="DELNODE"
                    remove_msg["Nodes"][0]=receFromNode_str["Node"]
                    Publisher_action.PublisherManager.MQTT_PublishMessage(remove_msg,_g_cst_MQTTAcTopicName)#Send a information about Removing nodes
                    _g_nodeList.remove(nodeinfo)
            return
    try:
        GWServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Socket開啟
    except socket.error, msg:
        print("[ERROR] Failed create Node listen socket! %s\n" % msg[1])
        sys.exit(1)

    GWServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Scoket開啟，並開始作接收、傳送的測試動作
    GWServerSocket.bind((_g_cst_NodeToGWSocketIP, _g_cst_NodeToGWSocketPort))
    GWServerSocket.listen(_g_cst_MaxNodeConnectionCount)

    print('===============================================')
    print('----------------Node->>>Gateway----------------\n')
    print('>>>Start listen Node %s<<<' % (time.asctime(time.localtime(time.time()))))
    print('===============================================\n')
    while True:
        (clientSocket, address) = GWServerSocket.accept()
        print("[INFO] Client Info: ", clientSocket, address)
        t = Thread(target=clientServiceThread, args=(clientSocket,))
        t.start()

t_NodeGateway = Thread(target=NodeToGatewaySocketThread, args=())
t_NodeGateway.start()



MQTT_Thread = Thread(target=GatewayToServerMQTTThread(),args=())
MQTT_Thread.start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
