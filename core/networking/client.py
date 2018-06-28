# client code
import socket
import datetime
from .utils import Formatter
from .encryption import Encryption
from .peer import PeerInfo

class Client:

    def __init__(self, myid,ip="127.0.0.1", port=4444):
        self.clients = {}  # dict {id:(conn_Handler)}
        self.id = myid
        self.ip = ip
        self.port = int(port)                
        self.tasks = {}#peerid:msg
        self.enc = Encryption()
            
    def CancelTask(self,peer_id):
        del self.tasks[peer_id]

    def PreformTask(self,peer_id,endpoint):
        msg = self.tasks[peer_id]
        self.Connect(endpoint,peer_id)
        self.SendToPeer(peer_id,msg)
        del self.tasks[peer_id]

    def Connect(self, endpoint, peer_id,pubk=None):
        if peer_id in self.clients:
            return
        try:
            conn = Conn_Handler(endpoint, peer_id, (self.ip, self.port), self.enc, pubk)
            self.clients[str(peer_id)] = conn
        except Exception as e:
            print(e)

    def DeleteConnection(self,peer_id):
        self.clients[peer_id].close_connection()
        del self.clients[peer_id]

    def GetPeer(self, peerid):

        if peerid in self.clients:
            return self.clients[peerid]
        return None

    def GetPeers(self):

        return self.clients.keys

    def NumberOfPeers(self):

        return len(self.clients)

    def SendToPeer(self, peer_id, msg):
        peer = self.GetPeer(peer_id)
        if not peer:
            self.tasks[peer_id] = msg
            return
        peer.send(msg)


class Conn_Handler:
    def __init__(self, endpoint, peer_id, myendpoint,enc,pubk=None):
        sock = socket.socket()
        self.conn = sock.connect(endpoint)
        self.id = peer_id
        self.endpoint = myendpoint #tuple of (ip,port)
        self.enc = enc
        self.hispubk = pubk

    def makemsg(self, data):
        packet = {"From": self.id, "Date": str(datetime.datetime.now()), "endpoint": self.endpoint}
        if self.hispubk:
            data = Formatter.EncodeJson(data)
            packet.update(self.enc.encrypt(data,self.hispubk))        
            return Formatter.EncodeJson(packet)
        else:
            data.update({"pubk":self.enc.pubkey,"pubsig":self.enc.pubsig})
            return Formatter.EncodeJson(data.update(packet))

    def send(self, data):
        self.conn.send(self.makemsg(data))

    def close_connection(self):
        self.conn.close()


class PeerNotFound(BaseException):
    def __str__(self):
        return "PeerNotFound Exception"

