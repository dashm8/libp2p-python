# server code
import asyncio
from .utils import Formatter


class ServerTcp:
    def __init__(self, ip, port, router,enc):
        self.ip = ip
        self.port = port
        self.handlers = {"signup":self.signup_handler,"bootstrap":self.bootstrap_handler,"ping":self.ping_handler,
            "search":self.search_handler,"store":self.store_hander,"app":self.app_handler}
        self.router = router        
        self.apps = {}
        self.enc = enc

    async def handle_echo(self, reader, writer=None):
        data = await reader.read(2048)
        data = data.decode()
        data = Formatter.DecodeJson(data)
        datatype = data["datatype"]
        self.handlers[datatype](data)

    def Run(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_echo, self.ip, self.port, loop=loop)
        server = loop.run_until_complete(coro)
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

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
            self.client.AddClient(data["endpoint"],data["From"],data["pubk"],data["pubsig"])

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
    def app_handler(self, data):

        apptype = data["apptype"]
        self.apps[apptype](data)

    def encryption_handler(self,data):
        clear = self.enc.decrypt(data)
        clear = Formatter.DecodeJson(clear)
        datatype = clear["datatype"]
        self.handlers[datatype](clear)