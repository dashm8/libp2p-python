from networking.client import Client
from networking.server import ServerTcp
from networking.encryption import Encryption
import kademlia
import sys
from threading import Thread

#sys.argv[1] = username
#sys.argv[2] = port

enc = Encryption()
clt = Client(sys.argv[1],enc)
kad = kademlia.Router(10,clt)
srv = ServerTcp('0.0.0.0',int(sys.argv[2]),kad,enc)
t1 = Thread(target=srv.listen)
t1.start()
print("hello world")
