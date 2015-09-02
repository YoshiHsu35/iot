__author__ = 'Nathaniel'

import socket
import threading
import json
import time
import uuid

_g_GatewaySocketIP = 'localhost'
_g_GatewaySocketPort = 10000
_g_NodeUUID = uuid.uuid1()

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


def main():
    global socketClient
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect(('localhost', int(_g_GatewaySocketPort)))
    initREG()

    def readData():
        while True:
            data = socketClient.recv(1024)
            if data:
                print('Received: ' + data.decode('utf-8'))

    t1 = threading.Thread(target=readData)
    t1.start()


def initREG():
    initMSGObj = {'Node': "NODE-" + str(_g_NodeUUID), 'Control': 'REG', 'NodeFunction': 'IOs',
                  'Functions': ["LED1", "LED2", "SW1"]}
    initMSGSTR = json.dumps(initMSGObj)
    now = time.strftime("%c")
    print(now)
    print("[INFO] SendREGMSG:%s" % initMSGSTR)
    sendData(initMSGSTR)


def sendData(sendData):
    socketClient.send(sendData.encode('utf-8'))


##t2 = threading.Thread(target=sendData)
##t2.start()

if __name__ == '__main__':
    main()
