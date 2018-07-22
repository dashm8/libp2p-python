from ecdsa import SigningKey,NIST521p,VerifyingKey
from Crypto.Cipher import AES,PKCS1_v1_5
from Crypto import Random
from Crypto.Hash import SHA ,SHA512
from Crypto.PublicKey import RSA


class Encryption:
    def __init__(self):
        self.prvsig,self.pubsig = ECDSA.generate_keypair_sign()
        self.prvkey,self.pubkey = RSA_ENC.generate_keys()
        
    def encrypt(self,data,recp_pubk):
        packet = {"datatype":"encrypted"}
        key = Random.new().read(128)        
        encrypted = AES_ENC.encrypt(key,data)
        packet["iv"],packet["data"] = encrypted        
        key_enc = RSA_ENC.encrypt(recp_pubk,key)
        packet["key"] = key_enc
        packet["signiture"] = ECDSA.sign(self.prvsig,key_enc)        
        packet["pubsig"] = self.pubsig
        return packet

    def decrypt(self,data):
        key = RSA_ENC.decrypt(self.prvkey,data["key"])
        data = AES_ENC.decrypt(key,data["data"],data["iv"])
        if ECDSA.verify(data["pubsig"],data["key"],data["signiture"]):
            return data
        else:
            raise BrokenSigniture

class RSA_ENC:

    @staticmethod
    def generate_keys():
        key = RSA.generate(4096,Random.new().read)
        prvk = key.exportKey()
        pubk = key.publickey().exportKey()
        return (prvk,pubk)

    @staticmethod
    def encrypt(key,massage):
        hasher = SHA.new(massage.encode())
        asym = RSA.importKey(key)
        cipher = PKCS1_v1_5.new(asym)
        return cipher.encrypt(massage.encode()+hasher.digest())

    @staticmethod
    def decrypt(key,ciphertext):
        asym = RSA.importKey(key)
        dsize = SHA.digest_size
        sentinel = Random.new().read(15+dsize)
        cipher = PKCS1_v1_5.new(asym)
        massage = cipher.decrypt(ciphertext,sentinel)
        return massage

class ECDSA:

    @staticmethod
    def generate_keypair_sign():
        #https://github.com/warner/python-ecdsa readme.md
        sk = SigningKey.generate(curve=NIST521p)
        vk = sk.get_verifying_key()
        return (sk.to_string(),vk.to_string())#sk is private and vk is public

    @staticmethod
    def sign(sk,massage):
        sk_obj =  SigningKey.from_string(sk,curve=NIST521p)
        return sk_obj.sign(massage.encode())#signiture

    @staticmethod
    def verify(vk,massage,signiture):
        vk_obj = VerifyingKey.from_string(vk,curve=NIST521p)
        return vk_obj.verify(signiture,massage)#bool

    

class AES_ENC:
    @staticmethod
    def encrypt(key,cleartext):
        key = AES_ENC.fix_size(key)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key,AES.MODE_CFB,iv)
        return (iv,cipher.encrypt(cleartext.encode()))

    @staticmethod
    def decrypt(key,massage,iv):
        key = AES_ENC.fix_size(key)        
        cipher = AES.new(key,AES.MODE_CFB,iv)
        return cipher.decrypt(massage)

    @staticmethod
    def fix_size(text):
        crypto = SHA.new()
        crypto.update(text.encode())
        return crypto.hexdigest()


class BrokenSigniture(BaseException):
    pass
