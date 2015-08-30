__author__ = 'Nathaniel'

import socket
import threading

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
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('localhost',50000))

    def readData():
        while True:
            data = s.recv(1024)
            if data:
                print('Received: ' + data.decode('utf-8'))

    t1 = threading.Thread(target=readData)
    t1.start()

    def sendData():
        while True:
            intxt = input()
            s.send(intxt.encode('utf-8'))

    t2 = threading.Thread(target=sendData)
    t2.start()

if __name__ == '__main__':
    main()
