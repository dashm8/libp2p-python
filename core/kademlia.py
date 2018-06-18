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
        self.RoutingTable = {}  # this dictionary contains the peers that this peer is connected to and their range from this peer, the format is {"hashed_peer_id":((ip,port)),range from this peer)}
        # self.RoutingTable = {}  # this dictionary contains the peers who are this peer is connected to, the format is {"hashed_peer_id":hashed_peer_id}
        self.kmax = kmax
        self.k = 0
        self.ttl = 10


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
        # peer_id = hashlib.sha256(peer_username).hexdigest() wrong
        OtherRoutingTable = {}
        for i in self.RoutingTable:
            if i[2] > Utils.get_range(i[0], peer_id):  # i[2] == range of another peer from this peer
                OtherRoutingTable[i[0]] = i  # adding the peer to the new peer's Routing table
                del self.RoutingTable[i[0]]  # deleting the added peer from this peer's Routing table

        return OtherRoutingTable

    def closest_to_peer(self, peer_id):
        range = 915792089237316195423570985008687907853269984665640564039457584007913129639936
        # 2^256 with 9 at the start instead of 1
        for i in self.RoutingTable.keys():
            range1 = Utils.get_range(i, peer_id)
            if range1 < range:
                peer = i
                range = range1
        return peer #peer id

########################################################################################################################
class Router:
    def __init__(self,kmax,client):
        self.peer = Peer(kmax,client)

    def signup(self, endpoint_server, server_id):
        '''

        :param endpoint_server: the signing up peer's endpoint
        :param server_id: the signing up peer's id
        :return: void
        '''
        packet = {"datatype": "bootstrap", "action": "request"}
        self.peer.client.Connect(endpoint_server, server_id)
        self.peer.client.SendToPeer(server_id, packet)

    ####################################################################################################################
    def ping(self, peer_id):
        '''

        :param peer_id: the "pinged" peer's id
        :return: void
        '''
        packet = {"datatype": "ping", "action": "request"}
        self.peer.client.SendToPeer(peer_id, packet)

    def ping_reply(self, data):
        '''

        :param data: contains the info of the requester
        :return:
        '''
        packet = {"datatype": "ping", "action": "reply"}
        self.peer.client.SendToPeer(data["From"], packet)

    ####################################################################################################################
    def bootstrap_resp(self, new_peer_id, endpoint, RoutingTable):
        self.peer.RoutingTable[new_peer_id] = (endpoint, self.peer.get_range(new_peer_id))
        packet = {"datatype": "signup", "RoutingTable": RoutingTable}
        self.peer.client.Connect(endpoint, new_peer_id)
        self.peer.client.SendToPeer(new_peer_id, packet)

    ####################################################################################################################
    def start_search(self, peer_id):
        if peer_id in self.peer.RoutingTable.keys():
            self.peer.client.PreformTask(peer_id,self.peer.RoutingTable[peer_id][0])
        else:
            self.init_search_peer(peer_id)

    def init_search_peer(self, peer_id):
        '''
        handler needed - redirects the search
        :param peer_id: the searched peer's id
        :return: void
        '''
        peer = self.peer.closest_to_peer(peer_id)
        packet = {"datatype": "findpeer", "action": "init", "ttl": self.peer.ttl, "peer_id": peer_id,
                  "searcher_id": self.peer.id}
        self.peer.client.SendToPeer(peer, packet)

    def redirect_search_peer(self, data):
        '''
        handler needed - redirects the search
        :param data:
        :return:
        '''
        peer_id = data["peer_id"]
        if peer_id in self.peer.RoutingTable.keys():
            packet = {"datatype": "findpeer", "action": "found", "ttl": data["ttl"] - 1, "peer_id": data["peer_id"],
            "endpoint":self.peer.RoutingTable["peer_id"][0]}
            self.peer.client.SendToPeer(data["searcher_id"], packet)
        else:
            if data["ttl"] > 0:
                packet = {"datatype": "searchpeer", "action": "search", "searcher_id": data["searcher_id"],
                          "ttl": data["ttl"] - 1, "peer_id": data["peer_id"]}
                peer = self.peer.closest_to_peer(data["peer_id"])
                self.peer.client.SendToPeer(peer, packet)
            else:
                packet = {"datatype": "searchpeer", "action": "end", "searcher_id": data["searcher_id"],
                          "peer_id": data["peer_id"]}
                self.peer.client.SendToPeer(data["searcher_id"], packet)
    ####################################################################################################################

    def store(self,peer_id,endpoint):
        recv_peer = self.peer.closest_to_peer(peer_id)
        packet = {"datatype":"store","action":"store","peer_id":peer_id,"ttl":self.peer.ttl,"endpoint":endpoint}
        self.peer.client.SendToPeer(recv_peer,packet)

    def recv_store(self,data):
        to_store_id = data["peer_id"]
        range_from_me = self.peer.get_range(to_store_id)
        replace_id = self.peer.closest_to_peer(to_store_id)
        range_from_replace = self.peer.RoutingTable[replace_id][1]
        if range_from_me > range_from_replace:
            if data['ttl'] == 0:
                return            
            packet = {"datatype":"store","action":"store","peer_id":to_store_id,"ttl":data['ttl']-1,
                "endpoint":data["endpoint"]}
            self.peer.client.SendToPeer(replace_id,packet)
        else:
            self.peer.RoutingTable[to_store_id] = (data["endpoint"],range_from_me)

    



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
update
bootstrap
'''
