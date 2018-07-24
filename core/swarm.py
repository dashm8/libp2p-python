import hashlib
import os
from os.path import isdir,isfile,join,getsize
import socket
from datetime import datetime
from networking.utils import Formatter
import hashlib
from networking.peer import PeerInfo

class Swarm:

    _instance = None

    def initdata(self,peerid):
        self.files = {}# dict {<checksum>:torrentfile}
        self.trackers {}#peerid:Tracker
        self.peer_id = peerid
        self.routerfiles = []#files that iam hoding their owners router would be closest hash to sha256(file)

    def __new__(self,peerid):
        if not self._instance:#singleton
            self._instance = super(Swarm,self).__new__(self,peerid)
            self.initdata(peerid)
        return self._instance 

    def create_file(self,fname):        
        T = Torrent(self.peer_id)
        t.make_torrent_file(fname)
        return self.get_tracker()

    def seed(self,endpoint,file_hash):#means upload
        sock = socket.socket()
        sock.connect(endpoint)
        sock.send(self.files[file_hash].format())

    def leech(self):#means download
        '''
        dict {endpoing:finfostream}
        '''
        pass
    
    def create_tracker(self,finfo):
        #fstruct is a struct in the torrent file (you need the torrent to be the tracker)
        t = Tracker()
        self.trackers[finfo] = t



    
    

class Torrent:
    def __init__(self,peer_id):
        self.peer_id = peer_id

    def make_torrent_file(self,file=None,metadata=None):
        if not file:
            raise TypeError("at least one file must be provided")

        self.torrent = {}        
        self.torrent["file_struct"] = self.get_file_struct(file)         
        self.get_file_hash
        self.torrent["creation_date"] = int(str(datetime.utcnow()))
        self.torrent["peer_id"] = self.peer_id
        self.torrent["size"] = self.get_file_size(file)
        self.torrent["info_hash"] = self.get_info_hash(self.torrent["file_struct"])
        return torrent

    def write_torrent_file(self,fname,data):
        data = Formatter.EncodeJson(data)
        f = open(fname,'w')
        f.write(data)

    def set_tracker(self,torrent,tracker):
        torrent["tracker"] = tracker

    def get_file_struct(self,path):
        struct = {}
        if isdir(path):
            for name in os.listdir(path):
                if isdir(join(path + name)):                
                    struct["dir_" + join(path,name)] = self.get_file_struct(path + name + '/')
                else:
                    struct[join(path + name)] = self.get_file_hash(join(path + name))
            sh = hashlib.sha256()
            for _,v in struct.items():
                if type(v) == type(dict()):
                    print(path)
                    sh.update(v["info"].encode())
                else:
                    sh.update(v.encode())
            struct["info"] = sh.hexdigest()            
        else:
            struct[path] = self.get_file_hash(path)        
        return struct

    def get_file_hash(self,path):
        #checksum of a file
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()


    def get_file_size(self,path):
        return getsize(path)

    def get_info_hash(self,struct):
        return struct["info"]


class Tracker:
    def __init__(self,torrent=None):
        owners = {} #peer_id:PeerInfo
        self.torrent = torrent
        
    def set_torrent(self,torrent):
        self.torrent = torrent

    def add_owner(self,peer_id,PeerInfo):
        owners[peer_id] = PeerInfo

    def get_owners(self):
        return owners
    

    

        
