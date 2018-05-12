#server code
import asyncio
import utils

class ServerAsync(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        massage = utils.Formatter.DecodeJson(message)
        message = massage["msgtype"]
        

        
    def connection_lost(self,exc):
        #logger
        self.transport.close()

class ServerTcp:

    def __init__(self,ip,port):
        self.handlers = {}
        self.ip = ip
        self.port = port


    def AddHandler(self,msgtype,handler):#str(msgtype)
        self.handlers[msgtype] = handler

        '''
        {"msgtype":<msgtype>}
        '''


    def Run(self):
        loop = asyncio.get_event_loop()#pool threads        
        coro = loop.create_server(ServerAsync, self.ip, self.port)
        server = loop.run_until_complete(coro)        
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()