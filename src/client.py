import socket
from cryptofunc import dump_private, dump_public, load_private,\
    load_public, decrypt, encrypt, generate_priv_key, exchange, get_shared_key
from json import load

with open('Factor.json', 'r') as f:
    json = load(f)
    response_port = json['response_port']
    continuance = json['continuance_probability']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), response_port))

privkey, sharedkey = get_shared_key(s)