from websocket_server import WebsocketServer
from threading import Thread
import socket
import sys
import time
import json

_g_cst_serverName = "SV1"

_g_cst_SVSocketServerIP = '' #不用特別指定的話就是接受所有INTERFACE的IP進入 
_g_cst_SVSocketServerPort = 50005 
_g_cst_MaxGatewayConnectionCount = 10
_g_cst_GatewayConnectionTimeOut = 1000

_g_cst_webSocketServerIP = '' #不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_webSocketServerPORT = 8009  
 
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":'######::'########:'########::'##::::'##:'########:'########::")
print("'##... ##: ##.....:: ##.... ##: ##:::: ##: ##.....:: ##.... ##:")
print(" ##:::..:: ##::::::: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##:")
print(". ######:: ######::: ########:: ##:::: ##: ######::: ########::")
print(":..... ##: ##...:::: ##.. ##:::. ##:: ##:: ##...:::: ##.. ##:::")
print("'##::: ##: ##::::::: ##::. ##:::. ## ##::: ##::::::: ##::. ##::")
print(". ######:: ########: ##:::. ##:::. ###:::: ########: ##:::. ##:")
print(":......:::........::..:::::..:::::...:::::........::..:::::..::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")

########### Normal Socket to Nodes ##############

_g_gatewayList = []

#listen to device socket connection
def serverSocketThread(): 
        devicePollingInterval = 1

        def clientServiceThread(client): 
             
            gatewayInfo = []
            gatewayInfo.append(client)
             
            ClientRegisted = False
                
            while(True):
                    time.sleep(devicePollingInterval)
                          
                    _str_recvMsg = client.recv(256)
                    _str_decodeMsg = _str_recvMsg.decode('utf-8')
                      
                        
                    print("[MESSAGE] Reciving message from [Gateway] at %s : \n >>> %s <<<" %(time.asctime(time.localtime(time.time())), _str_recvMsg))
                    
                    try:
                        _obj_json_msg = json.loads(_str_recvMsg)
                        
                        _obj_json_msg["Server"] = _g_cst_serverName

                        if not ClientRegisted:
                            gatewayInfo.append(_obj_json_msg["Gateway"])

                            #將此GW加入GW清單中
                            _g_gatewayList.append(gatewayInfo)
                            print ("[REGISTE] Gateway %s" % gatewayInfo) 
                            ClientRegisted = True
                             
                    except:
                        print("[ERROR] Couldn't converte json to Objet!")

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
        serverSocket.bind((_g_cst_SVSocketServerIP, _g_cst_SVSocketServerPort))
        serverSocket.listen(_g_cst_MaxGatewayConnectionCount)
        #serverSocket.settimeout(_g_cst_GatewayConnectionTimeOut)

        print('===============================================\n')
        print('---------------Gateway->>>Server---------------\n')
        print('>>>Start listen Gateways %s<<<' %(time.asctime(time.localtime(time.time()))))
        print('===============================================\n')
         

        while True:
            (clientSocket, address) = serverSocket.accept()
            print("[INFO] Client Info: ", clientSocket, address)
            t = Thread(target=clientServiceThread,args=(clientSocket,))
            t.start()


t = Thread(target = serverSocketThread,args = ())
t.start()

  
_g_instructionBuffer = [] 

########### WebSocket to SV ##############
 
# Called for every client connecting (after handshake)
def new_client(client, server):
    print('===============================================')
    print('---------------Gateway->>>Server---------------\n')
    print(">>>New client connected and was given id %d, handler %s, address %s<<<" %( client['id'], client['handler'], client['address']))
    print('===============================================\n') 

    #server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client,"Hi webclient") 

# Called for every client disconnecting
def client_left(client, server):
	print("[INFO] Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message): 
        if len(message) > 200:
                message = message[:200] + '..'
        print("[INFO] Client(%d) said: %s" % (client['id'], message))
        _g_instructionBuffer.append(message)
                        

server = WebsocketServer(_g_cst_webSocketServerPORT, _g_cst_webSocketServerIP)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()