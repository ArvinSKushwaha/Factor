import socket
from cryptofunc import dump_private, dump_public, load_private,\
    load_public, decrypt, encrypt, generate_priv_key, exchange, get_shared_key,\
    message_to_bytes, bytes_to_message
from json import load

with open('Factor.json', 'r') as f:
    json = load(f)
    response_port = json['response_port']
    continuance = json['continuance_probability']

def factor_client(ip_address, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.56.1', response_port))
    privkey, sharedkey = get_shared_key(client_socket)
    data = message_to_bytes(ip_address, message)
    data = encrypt(sharedkey, data)
    client_socket.send(data)
    full_msg = b''
    while True:
        msg = client_socket.recv(8192)
        if(msg == b''):
            break
        full_msg += msg
    content = decrypt(sharedkey, full_msg)
    return content

content = factor_client('127.0.0.1', 'https://google.com')
print(content)
with open('file.html', 'wb') as f:
    f.write(content)