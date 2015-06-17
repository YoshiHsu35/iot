__author__ = 'Nathaniel'

class NodeObj():
    Node=""
    IOs = []

class GatewayObj():
    Name=""
    Nodes=[]
    def __init__(self, GWName):
        self.Name = GWName
