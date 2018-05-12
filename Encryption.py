import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# Message encryption
'''
both private & public keys are the RECEIVER keys, the private key would be obtained by...
'''


def encrypt_text(text, pubkey):
    # pubkey is the Public Key of the RECEIVER
    key = RSA.importKey(pubkey)
    cipher = PKCS1_OAEP.new(key)
    encrypted_text = cipher.decrypt(text)
    return encrypted_text


def decrypt_text(text, privkey):
    # privkey is the Public Key of the RECEIVER
    key = RSA.importKey(privkey)
    cipher = PKCS1_OAEP.new(key)
    decrypted_text = cipher.decrypt(text)
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
