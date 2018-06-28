import hashlib
from .utils import Formatter

class PeerInfo:
    def __init__(self,endpoint,peer_id,pubk,pubsig,dist):
        self.endpoint = endpoint
        self.peer_id = peer_id
        self.pubk = pubk
        self.pubsig = pubsig        


    def fromString(self,peer):
        #string returned from __str__ of peer
        json = Formatter.DecodeJson(peer)
        self.endpoint = json["endpoint"]
        self.peer_id = json["peer_id"]
        self.pubk = json["pubk"]
        self.pubsig = json["pubsig"]

    def format(self):
        return {"endpoint":self.endpoint,"peer_id":self.peer_id,"pubk":self.pubk,"pubsig":self.pubsig}

    def __str__(self):
        json = self.format()
        return Formatter.EncodeJson(json)
