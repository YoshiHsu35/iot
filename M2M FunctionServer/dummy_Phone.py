__author__ = 'Nathaniel'
from class_MQTTManager import *
import time


def dummy_reg():
    publisherManager = PublisherManager()

    # time.sleep(.5)
    # publisherManager.MQTT_PublishMessage("FS1", '{"Gateway": "GW1","Control":"REQTOPICLIST"}')
    # time.sleep(.5)
    # publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"GETRULE"}')
    # time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Control": "ADDRULE","Rules": '
                                                '[{"RuleID": "4","InputGW": "GW3","InputNode": "N1",'
                                                '"InputIO": "SW1","OutputGW": "GW2","OutputNode": "N2",'
                                                '"OutputIO": "LED3","OutputValue": "1"}]}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"GETRULE"}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Control": "UPDATERULE","Rules": [{"RuleID": "1", '
                                                '"InputGW": "GW1","InputNode": "N1", "InputIO": "SW1",'
                                                '"OutputGW": "GW10","OutputNode": "N2","OutputIO": "LED3",'
                                                '"OutputValue": "1"}]}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Control": "DELRULE","Rules": [{"RuleID": "2"}]}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"GETRULE"}')


def main():
    dummy_reg()


if __name__ == '__main__':
    main()
