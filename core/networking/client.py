#client code
import socket
import datetime

class Client:


    def __init__(self,clients,id,router,ip="127.0.0.1",port=4444):
        self.clients = clients#dict {id:(conn)}
        self.id = id
        self.ip = ip
        self.port = port
        self.router = router#callable function


    def Connect(self,endpoint,peerid):

        try:
            conn = Conn_Handler(endpoint,peerid)
            self.clients[str(peerid)] = conn
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
        peer.send(msg)
        
        

class Conn_Handler:
    def __init__(self,endpoint,peerid):
       
        sock = socket.socket()
        self.conn = sock.connect(endpoint)
        self.id = peerid

    def makemsg(self,data):
        packet = {"From":self.id,"Date":str(datetime.datetime.now())}
        return data.update(packet)

    def send(self,data):
        self.conn.send(self.makemsg(data))

    


class PeerNotFound(BaseException):
    def __str__(self):
        return "PeerNotFound Exception"


        


