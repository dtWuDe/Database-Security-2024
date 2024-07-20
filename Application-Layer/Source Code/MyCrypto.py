import rsa
import configparser
from hashlib import sha1

def genKeyRSA(pub_name, file_name):
    Kpublic, Kprivate = rsa.newkeys(512)
    return Kpublic, Kprivate

def encryptRSA(string, pubKey):
    cipherText = rsa.encrypt(string.encode(), pubKey)
    return cipherText

def get_Krivate(pub_name, file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    n = config.get(pub_name, 'n')
    e = config.get(pub_name, 'e')
    d = config.get(pub_name, 'd')
    p = config.get(pub_name, 'p')
    q = config.get(pub_name, 'q')
    Kprivate = rsa.PrivateKey(int(n), int(e), int(d), int(p), int(q))
    config.clear()
    return Kprivate
    None

def get_Kpublic(pub_name, file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    n = config.get(pub_name, 'n')
    e = config.get(pub_name, 'e')
    Kprivate = rsa.PublicKey(int(n), int(e))
    config.clear()
    return Kprivate

def decryptRSA(string, privKey):
    plainText = rsa.decrypt(string, privKey)
    plainText = plainText.decode()
    return plainText

def write_key(file_name, pub_name, Kprivate):
    config = configparser.ConfigParser()
    config[pub_name] = {
        "n": Kprivate.n,
        "e": Kprivate.e,
        "d": Kprivate.d,
        "p": Kprivate.p,
        "q": Kprivate.q
    }
    with open(file_name, 'a') as file:
        config.write(file)
    
    config.clear()

def hash_sha1(str):
    hash_value = '0x' + sha1(str.encode('utf-8')).hexdigest()
    return hash_value

# get_Krivate('NV02PUB', 'EMP_PUB.key')