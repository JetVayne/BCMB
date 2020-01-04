import json
import socket


# ult save chain data
def save_chain(chain: dict):
    with open('download_chain.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(chain, indent=4))


# ult save user comment chain data
def save_comment(data: dict):
    with open('my_comment.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data, indent=4))


# ult create key files
def create_key_files(d: dict):
    if d.get('userKey'):
        with open('user.pem', 'w') as f:
            f.write(d.get('userKey'))

    if d.get('publicKey'):
        with open('public.pem', 'w') as f:
            f.write(d.get('publicKey'))

    if d.get('privateKey'):
        with open('private.pem', 'w') as f:
            f.write(d.get('privateKey'))


# ult create socket
def create_socket() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)
    s.settimeout(None)

    return s
