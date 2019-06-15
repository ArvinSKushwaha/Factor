import socket
import threading
import time

from cryptofunc import dump_private, dump_public, load_private,\
    load_public, decrypt, encrypt, generate_priv_key, exchange, get_shared_key,\
    message_to_bytes, bytes_to_message
from json import load

with open('Factor.json', 'r') as f:
    json = load(f)
    request_port = json['request_port']
    proxy_port = json['proxy_port']
    continuance = json['continuance_probability']

def factor_client(ip_address, message, method):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((socket.gethostname(), request_port))
    privkey, sharedkey = get_shared_key(client_socket)
    data = message_to_bytes(ip_address, message, method)
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

def reciever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), request_port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(10)
    while True:
        client_socket, address = server_socket.accept()
        print(address)
        privkey, sharedkey = get_shared_key(client_socket)
        data = client_socket.recv(8192)
        data = decrypt(sharedkey, data)
        ip, data, method = bytes_to_message(data)
        if(method == b'GET'):
            content = encrypt(sharedkey, requests.get(data).content)
        if(method == b'POST'):
            content = encrypt(sharedkey, requests.get(data).content)
        client_socket.send(content)
        client_socket.close()

def transmitter():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), proxy_port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(10)
    while True:
        client_socket, address = server_socket.accept()
        data = client_socket.recv(8192)
        print(data)
        method, data = data.split(b'\r\n')[0].split(b' ')[:2]
        data = factor_client(socket.gethostbyname(socket.gethostname()), data, method)
        client_socket.send(data)

incoming_server_thread = threading.Thread(target = reciever)
time.sleep(1)
transmitter()

# content = factor_client('127.0.0.1', 'https://google.com')
# print(content)
# with open('file.html', 'wb') as f:
    # f.write(content)