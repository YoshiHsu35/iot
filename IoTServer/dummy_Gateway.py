__author__ = 'Nathaniel'
import class_MQTTManager
import time



def dummy_reg():
    publisherManager = class_MQTTManager.PublisherManager()
    publisherManager.MQTT_PublishMessage("IOTSV/REG2",'{ "Gateway": "GW1", "Control": "REG"}')
    time.sleep(3)
    publisherManager.MQTT_PublishMessage("GW1",'{"Gateway": "GW1","Control": "ADDNODE", "Nodes": [{    "Node": "N1",     "IOs": ["LED1",     "LED2",     "SW1"] }]}')

def main():
    dummy_reg()

if __name__ == '__main__':
        main()
