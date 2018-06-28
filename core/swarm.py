import hashlib
import os
import socket

class swarm:
    def __init__(self):
        self.files = {}# dict {<checksum>:finfo}
        self.routerfiles = []#files that iam hoding their owners router would be closest hash to sha256(file)

    def create_file(self,fname):
        f = finfo(fname)
        self.files[f.checksum] = f

    def seed(self,endpoint,file_hash):#means upload
        sock = socket.socket()
        sock.connect(endpoint)
        sock.send(self.files[file_hash].format())

    def leech(self):#means download
        '''
        dict {endpoing:finfostream}
        '''
        pass

class finfo:
    def __init__(self,fname):
        self.fname = fname
        self.length = self.file_size() # size in bytes
        self.checksum = self.checksum_calc() #file checksum might take sometime for large files
        self.piece_length = (256 * 1024) #256 Kilo bytes
        self.pieces_hash = self.pieces_hash_calc()
        

    def foramt_finfo(self):
        #<32 bytes checksum><36 bytes size of file><18 bytes number of chunks><18 bits for chunk owning>
        #706 bit massagte
        stream = ""
        stream += self.checksum.encode()#checksum bytes        
        stream += bytes([self.length])#size of the file
        piececount = self.add_padding()
        stream += bytes(piececount)#chunck count
        return stream

    def pieces_hash_calc(self):        
        ret = []
        with open(self.fname, "rb") as f:
            for chunk in iter(lambda: f.read(self.piece_length)):
                hash_sha1 = hashlib.sha1()
                hash_sha1.update(chunk)
                ret.append(hash_sha1.hexdigest())
        return ret

    def file_size(self):
        statinfo = os.stat(self.fname)
        return statinfo.st_size

    def checksum_calc(self):
        hash_sha256 = hashlib.sha256()
        with open(self.fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()


    def add_padding(self,st,count):
        return str(0 * (count-len(st))) + st
    



