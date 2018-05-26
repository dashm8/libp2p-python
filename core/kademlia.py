# this is gonna be ruff
import hashlib

'''
        self.clients = clients#dict {id:(conn)}
        self.id = id
        self.ip = ip
        self.port = port
        self.router = router#callable function
'''
class Peer:
    def __init__(self, kmax, client):
        '''
        :param kmax: the (most of the time) fixed size of the maximum amount of peers that one peer can hold.
        :param username: simply the peer's username, will be used in the generation of the peer's id.
        '''
        self.client = client
        self.id = hashlib.sha256(client.id).hexdigest()
        self.RoutingTable = {} # this dictionary contains the peers that this peer is connected to and their range from this peer, the format is {"hashed_peer_id":((ip,port)),range from this peer)}
        #self.RoutingTable = {}  # this dictionary contains the peers who are this peer is connected to, the format is {"hashed_peer_id":hashed_peer_id}
        self.kmax = kmax
        self.k = 0        

    def get_range(self, peer_id):
        '''

        :param peer_id: the other peer's id
        :return: the range from this peer to another peer
        '''
        my_id = int(self.id, 16)
        peeridb = int(peer_id, 16)
        return my_id ^ peeridb

    def add_peer(self, peer_id):  # might be add_friend
        '''

        :param peer_username: the new peer's username
        :return: this function doesn't return anything.
        this function adds a new peer to the tree, is the base "Sign up" function
        '''        
        #peer_id = hashlib.sha256(peer_username).hexdigest() wrong
        OtherRoutingTable = {}
        for i in self.RoutingTable:
            if i[2] > Utils.get_range(i[0],peer_id):           #i[2] == range of another peer from this peer
                OtherRoutingTable[i[0]] = i                    # adding the peer to the new peer's Routing table
                del self.RoutingTable[i[0]]                    # deleting the added peer from this peer's Routing table
        return OtherRoutingTable



        self.RoutingTable[peer_id] = (endpoint,self.get_range(peer_id))


    



        


class Router:
    def __init__(self):
        self.peer = Peer()

    def signup(self,endpoint_server,server_id):
        packet = {"datatype":"bootstrap","action":"request"}
        self.peer.client.Connect(endpoint_server,server_id)
        self.peer.client.SendToPeer(server_id,packet)

    

    def bootstrap_resp(self,new_peer_id,endpoint):
        



class RouterProtocol:
    print("do stuff")


class Utils:

    @staticmethod
    def get_range(peerida, peeridb):
        peerida = int(peerida, 16)
        peeridb = int(peeridb, 16)
        return peerida ^ peeridb
'''
death signal -> temp table
ping
store
add
divide
updatek
bootstrap
'''