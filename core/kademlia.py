#this is gonna be ruff
import hashlib

class Peer:
    def __init__(self,kmax,username):
        self.id = hashlib.sha256()
        self.RoutingTable = {}
        self.kmax = kmax


    def GetKsize(self):
        return len(self.RoutingTable)

    def GetRange(self,peeridb):
        self.id = int(self.id,16)
        peeridb = int(peeridb,16)
        return self.id ^ peeridb




class Router:
    print("do stuff")

class Utils:

    @staticmethod
    def GetRange(peerida,peeridb):
        peerida = int(peerida,16)
        peeridb = int(peeridb,16)
        return peerida ^ peeridb

