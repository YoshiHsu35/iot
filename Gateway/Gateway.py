from threading import Thread
import socket
import sys
import time
import json

_g_cst_gatewayName = "GW1"

_g_cst_ToServerSocketIP = "127.0.0.1"
_g_cst_GWSocketServerPort = 50005

_g_cst_NodeToGWSocketIP = '' #不用特別指定的話就是接受所有INTERFACE的IP進入
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
     
    while(not _b_isEstablishedConnect): 
        try:
            ToServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)
 
        try:
            ToServerSocket.connect((_g_cst_ToServerSocketIP, _g_cst_GWSocketServerPort))

            #若與server連線建立成功，把這個連線存到server list，讓其他的部分可以調用傳訊息上Server
            _g_serverList.append(ToServerSocket) 
            _b_isEstablishedConnect = True
            print('===============================================\n')
            print('---------------Gateway->>>Server---------------\n')
            print('>>>Start connect Server %s<<<' %(time.asctime(time.localtime(time.time()))))
            print('===============================================\n')
        except socket.error, msg:
            sys.stderr.write("[ERROR] Failed connecting to Server! %s\n" % msg[1])
            exit(1) 

        #向Server註冊
        ToServerSocket.send('{"Gateway":%s, "Control":REG}' %(_g_cst_gatewayName)) 
         

t_GatewayServer = Thread(target = GatewayToServerSocketThread,args = ())
t_GatewayServer.start()
  

########### Normal Socket to Nodes(As socket Server) ##############

_g_nodeList = []
 
def NodeToGatewaySocketThread(): 
      
        devicePollingInterval = 1 

        def clientServiceThread(client): 

            #若node連線建立成功，把這個連線存到node list，讓其他的部分可以調用傳訊息
            _g_nodeList.append(client)
                
            while(True):
                    time.sleep(devicePollingInterval)

                    #if len(_g_instructionBuffer)==0:
                    #        client.send(_str_recvMsg+"\n")
                    #else:
                    #        finalDecision=_g_instructionBuffer.pop()
                    #        _g_instructionBuffer=[]
                    #        client.send(finalDecision.decode('utf-8')+"\n")
                        
                    _str_recvMsg = client.recv(256)
                    _str_decodeMsg = _str_recvMsg.decode('utf-8')
                         
                    #server.send_message(client, _str_recvMsg)

                        
                    ## _str_recvMsg["Gateway"] = "GW1";
                        
                    print("[MESSAGE] Reciving message from [Node] at %s : \n >>> %s <<<" %(time.asctime(time.localtime(time.time())), _str_recvMsg))
                          
                    #data = {
                    #    'name' : 'ACME',
                    #    'shares' : 100,
                    #    'price'  : 542.23
                    #    }
                    #json_str = json.dumps(data)

                    #print(json_str)
                    #data = json.loads(json_str) 
                    #print(data)
                        
                    try:
                        #將文字轉成object
                        _obj_json_msg = json.loads(_str_recvMsg)
                        
                        #插入新的attribute
                        _obj_json_msg["Gateway"] = _g_cst_gatewayName

                        #轉成文字
                        _str_sendToSvJson = json.dumps(_obj_json_msg)
                                                                    
                    except:
                        print("[ERROR] Couldn't converte json to Objet!")
                         
                    #從ServerList裡面挑第一個Server送Json字串上去
                    _g_serverList[0].send(_str_sendToSvJson)
                         


        try:
            GWServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] Failed create Node listen socket! %s\n" % msg[1])
            sys.exit(1)

        GWServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
        GWServerSocket.bind((_g_cst_NodeToGWSocketIP, _g_cst_NodeToGWSocketPort))
        GWServerSocket.listen(_g_cst_MaxNodeConnectionCount)
        #GWServerSocket.settimeout(_g_cst_NodeConnectionTimeOut)

        print('===============================================')
        print('----------------Node->>>Gateway----------------\n')
        print('>>>Start listen Devices %s<<<' %(time.asctime(time.localtime(time.time()))))
        print('===============================================\n')

        while True:
            (clientSocket, address) = GWServerSocket.accept()
            print("[INFO] Client Info: ", clientSocket, address)
            t = Thread(target=clientServiceThread,args=(clientSocket,))
            t.start()


t_NodeGateway = Thread(target = NodeToGatewaySocketThread,args = ())
t_NodeGateway.start()


