import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

# AES - key  encryption
'''
functions that encrypt the AES key
#both private & public keys are the RECEIVER keys, the private key would be obtained by...
'''


def encrypt_key(text, pubkey):
    # pubkey is the Public Key of the RECEIVER
    key = RSA.importKey(pubkey)
    cipher = PKCS1_OAEP.new(key)
    encrypted_key = cipher.decrypt(text)
    return encrypted_key


def decrypt_key(text, privkey):
    # privkey is the Public Key of the RECEIVER
    key = RSA.importKey(privkey)
    cipher = PKCS1_OAEP.new(key)
    decrypted_key = cipher.decrypt(text)
    return decrypted_key


# AES message Encryption

def encrypt_text(text, pubkey, key_byts=32):
    # pubkey is the Public Key of the RECEIVER
    key = encrypt_key(Random.get_random_bytes(32), pubkey)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_text = iv + cipher.encrypt(text)
    return encrypted_text


def decrypt_text(text, privkey):
    # privkey is the Public Key of the RECEIVER
    key = decrypt_key(Random.get_random_bytes(32), privkey)
    iv = text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_text = cipher.decrypt(text[AES.block_size:])
    return decrypted_text


class RSA_Keys():

    # class that generates the RSA Public and Private Keys

    def __init__(self, Public_key=None, Private_key=None):
        self.Public_key = Public_key
        self.Private_key = Private_key  # change it later to self.__Private_key to prevent access to the attribute,
        # https://stackoverflow.com/questions/4555932/public-or-private-attribute-in-python-what-is-the-best-way

    def generate_new_keys(self, bits=2048):
        if (bits % 256 != 0) and (bits < 1024):
            return "Error"
        keys = RSA.generate(bits)
        self.Private_key = keys.exportKey('DER')
        self.Public_key = keys.publickey().exportKey('DER')
