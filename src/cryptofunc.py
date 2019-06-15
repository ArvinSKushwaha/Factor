from os import urandom
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, ECDH, generate_private_key, SECP256K1
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat, NoEncryption, Encoding,\
    load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CTR
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA3_256
from requests import get

def exchange(privkey, pubkey):
    return privkey.exchange(ECDH(), pubkey)

def generate_priv_key():
    return generate_private_key(SECP256K1, default_backend())

def dump_private(key):
    return key.private_bytes(
        encoding = Encoding.PEM,
        format = PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = NoEncryption()
    )

def dump_public(key):
    return key.public_bytes(
        encoding = Encoding.PEM,
        format = PublicFormat.SubjectPublicKeyInfo
    )

def load_private(bytestring):
    return load_pem_private_key(bytestring, None, default_backend())

def load_public(bytestring):
    return load_pem_public_key(bytestring, default_backend())

def encrypt(key, data):
    nonce = urandom(16)
    key256 = HKDF(SHA3_256(), 32, nonce, None, default_backend()).derive(key)
    cipher = Cipher(AES(key256), CTR(nonce), default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize() + nonce

def decrypt(key, encrypted):
    nonce = encrypted[-16:]
    data = encrypted[:-16]
    key256 = HKDF(SHA3_256(), 32, nonce, None, default_backend()).derive(key)
    cipher = Cipher(AES(key256), CTR(nonce), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

def get_shared_key(s):
    privkey = generate_priv_key()
    pubkey = privkey.public_key()
    s.send(dump_public(pubkey))
    data = s.recv(8192)
    pubkey = load_public(data)
    return (privkey, exchange(privkey, pubkey))

def message_to_bytes(ip, data, method):
    ip = bytes(ip, 'utf-8')
    data = bytes(data, 'utf-8')
    return ip+b"__!@#$%^&*()__"+data+b"__!@#$%^&*()__"+method

def bytes_to_message(message):
    ip, data, method = message.split(b"__!@#$%^&*()__")
    return ip, data, method