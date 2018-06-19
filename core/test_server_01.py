from networking.client import Client
from networking.server import ServerTcp
import kademlia

clt = Client("username")
kad = kademlia.Router(10,clt)
srv = ServerTcp('0.0.0.0',4444,kad)
srv.Run()
print("done")