__author__ = 'Nathaniel'
from .class_MQTTManager import *
import time


def dummy_reg():
    publisherManager = PublisherManager()
    for x in range(1, 4):
        publisherManager.MQTT_PublishMessage("IOTSV/REG", '{ "Gateway": "GW%s", "Control": "GWREG"}' % (x))
        time.sleep(1)

    publisherManager.MQTT_PublishMessage("GW1",
                                         '{"Gateway": "GW1","Control": "ADDNODE", '
                                         '"Nodes": [{"Node": "N1","NodeFunction":"IOs", '
                                         '"Functions": ["LED1","LED2", "SW1"]},'
                                         '{"Node": "N2","NodeFunction":"IOs", "Functions": ["MOTO","LED2", "SW1"]}]}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("GW2",
                                         '{"Gateway": "GW2","Control": "ADDNODE", '
                                         '"Nodes": [{"Node": "N3","NodeFunction":"IOs", '
                                         '"Functions": ["LED3","LED4", "SW2"] },'
                                         '{"Node": "N22","NodeFunction":"IOs", "Functions": ["MOTOx"]}]}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("GW3",
                                         '{"Gateway": "GW3","Control": "ADDNODE", '
                                         '"Nodes": [{"Node": "N2","NodeFunction":"IOs", '
                                         '"Functions": ["LED5","LED6", "SW3"] },'
                                         '{"Node": "N9","NodeFunction":"IPCams", '
                                         '"Functions": ["CAM1","CAM2"] }]}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("GW1", '{"Gateway": "GW1","Control": "DELNODE", "Nodes": ["N2"]}')


def main():
    dummy_reg()


if __name__ == '__main__':
    main()
