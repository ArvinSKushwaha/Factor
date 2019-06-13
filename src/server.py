import socket
from json import load
from cryptofunc import dump_private, dump_public, load_private,\
    load_public, decrypt, encrypt, generate_priv_key, exchange, get_shared_key
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), response_port))
s.listen(5)
while True:
    clientsocket, address = s.accept()
    print(address)
    privkey, sharedkey = get_shared_key(clientsocket)