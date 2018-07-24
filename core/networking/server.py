# server code
import socket
from .utils import Formatter
import threading
from time import sleep
from encryption import Encryption
from swarm import Swarm

class ServerTcp:
    def __init__(self, ip, port, router):
        self.ip = ip
        self.port = port
        #init socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        #init handlers
        self.handlers = {"bootstrap":self.bootstrap_handler,"ping":self.ping_handler,
            "search":self.search_handler,"store":self.store_hander,"app":self.app_handler,
            "encrypted":self.encryption_handler}
        self.router = router        
        self.apps = {}
        self.enc = Encryption()
        self.flag = True

    def listen(self):
        self.sock.listen(5)
        print("server is runing on port: " + str(self.port))
        while self.flag:
            client,_ = self.sock.accept()
            client.settimeout(30)
            threading.Thread(target=self.handle,args=client)

    def handle(self,client):
        while self.flag:
            try:
                data = client.recv(2048)
                data = Formatter.DecodeJson(data)
                datatype = data["datatype"]
                self.handlers[datatype](data)
                sleep(0.5)
            except Exception:
                client.close()

    def add_handlers(self,handlers):
        self.handlers.update(handlers)

    def stop(self):
        #stops the server
        self.flag = False


########################################################################################################################
    def bootstrap_handler(self, data):
        '''
        :param data: contains the data for requesting bootstrap
        :return: void - leads to the creation of the new user's routing table
        '''
        action = data["action"]
        if action == "request":            
            peer = data["peer_id"]
            range_from_peer = self.router.peer.get_range(peer)
            new_peer = self.router.peer.closest_to_peer(peer)
            range_from_new_peer = self.router.peer.get_range(new_peer)
            if range_from_new_peer < range_from_peer:
                self.router.bootstrap_red(data,new_peer)
            else:
                RoutingTable = self.router.peer.add_peer(data["From"])
                self.router.bootstrap_resp(data,RoutingTable)
        elif action == "response":
            RoutingTable = data["RoutingTable"]
            self.router.peer.RoutingTable = RoutingTable
        elif action == "redirect":
            RoutingTable = self.router.peer.add_peer(data["peer_id"])
            self.router.bootstrap_resp_red(data,RoutingTable)

########################################################################################################################
    def ping_handler(self, data):
        '''

        :param data: contains the data for
        :return:
        '''
        if data["action"] == "request":
            self.router.ping_reply(data)
        else:
            print(data["From"] + " is alive")
            self.router.client.AddClient(data["endpoint"],data["From"],data["pubk"],data["pubsig"])

########################################################################################################################
    def search_handler(self, data):
        action = data["action"]
        if action == "found":
            self.router.peer.client.PreformTask(data["peer_id"],data["endpoint"])
        if action == "init":
            self.router.redirect_search_peer(data)
        if action == "search":
            self.router.redirect_search_peer(data)
        if action == "end":
            self.router.peer.client.CancelTask(data["peer_id"])


########################################################################################################################
    def store_hander(self,data):
        action = data["action"]
        if action == "store":
            self.router.recv_store(data)

########################################################################################################################
    def swarm_handler(self,data):
        action = data["action"]
        if action == "find_tracker":
            s = Swarm(self.router.peer.id)
            
########################################################################################################################
    def app_handler(self, data):

        apptype = data["apptype"]
        self.apps[apptype](data)

    def encryption_handler(self,data):
        clear = self.enc.decrypt(data)
        clear = Formatter.DecodeJson(clear)
        datatype = clear["datatype"]
        self.handlers[datatype](clear)