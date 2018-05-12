#server code
import asyncio
from utils import Formatter

class ServerTcp:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.handlers = {}
        
    async def handle_echo(self,reader, writer=None):
        data = await reader.read(2048)
        message = data.decode()
        message = Formatter.DecodeJson(message)
        print(message)
        msgtype = message["msgtype"]
        print(msgtype)
        self.handlers[msgtype]()
        print("all good")


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

    

