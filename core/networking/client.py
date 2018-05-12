#client code
import socket

class Client:


    def __init__(self,clients,id,router,ip="127.0.0.1",port=4444):
        self.clients = clients#dict {id:(conn)}
        self.id = id
        self.ip = ip
        self.port = port
        self.router = router#callable function


    def Connect(self,ip,port,id):

        try:
            sock = socket.socket()
            sock.connect(ip,port)
            self.clients[str(id)] = sock
        except Exception as e:
            print(e)

    def Route(self,peerid):

        (ip,port) = self.router(peerid)#should be async
        if not ip:
            return None
        return (ip,port)

    def GetPeer(self,peerid):

        if peerid in self.clients:
            return self.clients[peerid]
        return None

    def GetPeers(self):

        return self.clients.keys

    def NumberOfPeers(self):

        return len(self.clients)

    def SendToPeer(self,peerid,msg):
        peer = self.GetPeer(peerid)
        if not peer:
            peer = self.Route(peer)
            if not peer:
                raise PeerNotFound
        

class Peer:
    def __init__(self,ip,port,peerid):
        self.ip = ip
        self.port = port
        sock = socket.socket()
        self.conn = sock.connect((ip,port))
        self.id = peerid

    def _makemsg(self,data):
        return 

    def send(self,data):
        self.conn.send(data)

    


class PeerNotFound(BaseException):
    def __str__(self):
        return "PeerNotFound Exception"


        


