import socket
from json import load
from cryptofunc import dump_private, dump_public, load_private,\
    load_public, decrypt, encrypt, generate_priv_key, exchange, get_shared_key,\
    message_to_bytes, bytes_to_message
import requests

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

with open('Factor.json', 'r') as f:
    json = load(f)
    response_port = json['response_port']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), response_port))
server_socket.listen(10)
while True:
    client_socket, address = server_socket.accept()
    print(address)
    privkey, sharedkey = get_shared_key(client_socket)
    data = client_socket.recv(8192)
    data = decrypt(sharedkey, data)
    ip, data = bytes_to_message(data)
    content = encrypt(sharedkey, requests.get(data).content)
    client_socket.send(content)
    client_socket.close()