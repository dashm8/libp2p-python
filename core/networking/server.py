# server code
import asyncio
from utils import Formatter


class ServerTcp:
    def __init__(self, ip, port, router):
        self.ip = ip
        self.port = port
        self.handlers = {}
        self.router = router
        self.apps = {}

    async def handle_echo(self, reader, writer=None):
        data = await reader.read(2048)
        data = data.decode()
        data = Formatter.DecodeJson(data)
        datatype = data["datatype"]
        self.(self.handlers[datatype](data))

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
    def signup_handler(self, data):
        '''

        :param data: the returned data from the add_peer function that is in the peer class.
        :return: void
        setting up the new peer's Routing table
        '''
        RoutingTable = data["RoutingTable"]
        self.router.peer.RoutingTable = RoutingTable

    def bootstrap_handler(self, data):
        '''

        :param data: contains the data for requesting bootstrap
        :return: void - leads to the creation of the new user's routing table
        '''
        RoutingTable = self.router.peer.add_peer(data["From"])
        self.router.bootstrap_resp(data["From"], data["endpoint"], RoutingTable)

########################################################################################################################
    def ping_handler(self, data):
        '''

        :param data: contains the data for
        :return:
        '''
        if data["action"] == "request":
            self.router.ping_reply(data)
        else:
            print(data["From"] + "is alive")

########################################################################################################################
    def search_handler(self, data):
        action = data["action"]
        if action == "found":

        if action == "init":

        if action == "search":

        if action == "end":


########################################################################################################################

    def app_handler(self, data):

        apptype = data["apptype"]
        self.apps[apptype](data)
