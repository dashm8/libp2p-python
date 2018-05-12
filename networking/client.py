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
            print e

    def Route(self,id):
        (ip,port) = self.router(id)
        if not ip:
            return None
        return (ip,port)

    

        


