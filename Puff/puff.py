# coding: utf-8
import datetime
import hashlib
import sys
import ecdsa
import queue
import socket
import threading
import json
import time
import pandas as pd
from flask import Flask, request, abort
from collections import Counter

from ult.BMC import *
from ult.PCReply import *
from ult.PSV import *
from ult.SignUp import *
from ult.SingIn import *
from ult.tools import *

VERSION = '2.0'
app = Flask(__name__)
Block_Chain = []
DIFFICULTY = 5
member = pd.DataFrame(columns=['id', 'userKey', 'name', 'luckyNum', 'publicKey', 'privateKey', 'createDate'])

# HOST = 'ec2-34-234-194-147.compute-1.amazonaws.com'
HOST = 'localhost'
PORT = 7777

client_queue = queue.Queue(maxsize=100)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.bind((HOST, PORT))
s.listen(100)
print('BCMB Puff Server is started at ', HOST, '-', PORT)
print('Puff Version:', VERSION)

usher_flag = True
serve_flag = True
guard_flag = True
da_flag = True

push_count = 0


# socket serve space - start ###########################################################################################
# public thread
def serve():
    global client_queue
    print('[INFO] Serve Service is started.')
    while serve_flag:
        if not client_queue.empty():
            client = client_queue.get()
            client_request = json.loads(client.recv(8192).decode('utf8'))
            if client_request.get('service'):
                service_type = client_request.get('service')

                if service_type == '1':
                    reply = sign_up_helper(client_request)
                    client.send(bytes(reply, encoding='utf8'))
                    client.close()

                elif service_type == '2':
                    reply = sign_in_helper(client_request)
                    client.send(bytes(reply, encoding='utf8'))
                    client.close()

                elif service_type == '4':
                    reply = push_comment_helper(client_request)
                    client.send(bytes(reply, encoding='utf8'))
                    client.close()

                elif service_type == '6':
                    reply = get_rank_helper(client_request)
                    client.send(bytes(reply, encoding='utf8'))
                    client.close()

                elif service_type == 'a':
                    reply = get_BMC_helper(client_request)
                    reply = json.dumps(reply)
                    client.send(bytes(reply, encoding='utf8'))
                    client.close()

    print('[INFO] TASK - serve finished.')


# public helper 1
def sign_up_helper(job: dict) -> json:
    name = job.get('username')
    lucky_num = job.get('luckyNum')

    # create pub prv keys
    key_list = create_key()
    public_key = key_list[0]
    private_key = key_list[1]

    # create user key
    user_key = create_user_key(name, lucky_num, public_key)

    sign_up_reply = make_sign_up_reply(name, lucky_num, user_key, public_key, private_key)
    add_member(name, lucky_num, user_key, public_key, private_key)

    return sign_up_reply


# public tool 1
def add_member(name: str, lucky_num: str, user_key: str, public_key: ecdsa.VerifyingKey,
               private_key: ecdsa.SigningKey):
    global member
    record = list()
    record.append(len(member) + 1)
    record.append(user_key)
    record.append(name)
    record.append(lucky_num)
    record.append(str(public_key.to_pem(), encoding='utf-8'))
    record.append(str(private_key.to_pem(), encoding='utf-8'))
    record.append(datetime.datetime.now())

    member.loc[len(member)] = record


# public tool 1
def create_key() -> list:
    result = []
    flag = True
    while flag:
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.BRAINPOOLP160r1)
        public_key = private_key.verifying_key
        pvs = str(private_key.to_pem(), encoding='utf-8')
        pbs = str(public_key.to_pem(), encoding='utf-8')

        if pbs not in member['publicKey'].values and pvs not in member['privateKey'].values:
            result.append(public_key)
            result.append(private_key)
            flag = False

    return result


# public helper 2
def sign_in_helper(job: dict) -> json:
    reply = dict()
    uk = job.get('userKey')
    ln = job.get('luckyNum')
    if is_valid_user_key(uk):
        data = member.query('userKey==@uk')
        cln = data['luckyNum'].values[0]
        if ln == cln:
            return get_SIS_reply(data, uk, ln)
        else:
            return get_SIE_reply_b()
    else:
        return get_SIE_reply_a()


# public helper 4
def push_comment_helper(job: dict) -> json:
    uk = job.get('userKey')
    if not is_valid_user_key(uk):
        return get_PCE_reply_a()

    sig = job.get('signature')
    pbk = job.get('publicKey')
    comment = job.get('comment')
    if not check_PSV(sig, pbk, comment):
        return get_PCE_reply_b()

    nonce = job.get('nonce')
    if not check_proof(uk, nonce, comment):
        return get_PCE_reply_c()

    if is_first_person(job):
        new_hash = get_x_hash(uk, nonce, comment)
        author = job.get('author')
        pac = job.get('PAC')
        license = job.get('license')

        add_new_block(new_hash, author, comment, uk, nonce, pac, license, sig, pbk)
        return get_PCS_reply()

    else:
        return get_PCE_reply_d()


# public tool 4
def add_new_block(prev_hash: str, author: str, comment: str, user_key: str,
                  nonce: int, pac: str, license: str, signature: str, public_key: str):
    global Block_Chain
    block = dict()
    block['previous'] = prev_hash
    block['index'] = len(Block_Chain)
    block['author'] = author
    block['comment'] = comment
    block['timestamp'] = str(datetime.datetime.now())

    proof = dict()
    proof['userKey'] = user_key
    proof['nonce'] = str(nonce)
    proof['PAC'] = pac
    proof['license'] = license
    block['proof'] = proof

    psv = dict()
    psv['signature'] = signature
    psv['publicKey'] = public_key
    block['PSV'] = psv

    Block_Chain.append(block)


# public tool 4
def is_first_person(BCA: dict):
    pac = BCA.get('PAC')
    license = BCA.get('license')
    block_str = str(get_latest_block())
    curr_hash = get_MD5_code(block_str + pac)
    if curr_hash == license:
        return True
    else:
        return False


# public tool 4
def check_proof(user_key: str, nonce: int, comment: str):
    x_hash = get_x_hash(user_key, nonce, comment)
    if is_valid_x_hash(x_hash):
        return True
    else:
        return False


# public tool 4
def get_x_hash(user_key: str, nonce: int, comment: str):
    latest_block = get_latest_block()
    hs = latest_block.get('previous') + \
         str(latest_block.get('index')) + \
         latest_block.get('author') + \
         latest_block.get('comment') + \
         latest_block.get('timestamp') + \
         latest_block['proof'].get('userKey') + \
         latest_block['proof'].get('nonce') + \
         latest_block['proof'].get('PAC') + \
         latest_block['proof'].get('license') + \
         latest_block['PSV'].get('signature') + \
         latest_block['PSV'].get('publicKey') + \
         user_key + str(nonce) + comment

    hash = hashlib.sha256()
    hash.update(hs.encode('utf-8'))
    result = hash.hexdigest()

    return result


# public tool 4
def is_valid_x_hash(hash: str) -> bool:
    if hash[0:DIFFICULTY] == ''.join(['0'] * DIFFICULTY):
        return True
    else:
        return False


# public tool (4,a)
def get_latest_block() -> dict:
    return Block_Chain[-1]


# public helper 6
def get_rank_helper(job: dict) -> json:
    all_block_keys = get_all_cblock_user_key()
    count_result = Counter(all_block_keys)

    all_rank = count_result.most_common()
    rank = count_result.most_common(10)

    output = create_rank_reply(rank)
    user_rank = '--'

    uk = job.get('userKey')

    for i, p in enumerate(all_rank):
        if p[0] == uk:
            user_rank = str(i + 1)
            break

    output['userKey'] = uk
    output['userRank'] = user_rank

    return json.dumps(output)


# public tool 6
def create_rank_reply(data: list) -> json:
    result = dict()
    result['result'] = True
    result['lastUpdate'] = Block_Chain[-1]['timestamp']
    rank = []
    for i in data:
        uk = i[0]
        count = i[1]
        record = dict()
        record['userKey'] = uk
        mi = member.query('userKey==@uk')
        name = mi['name'].values[0]
        record['username'] = name
        record['times'] = count
        rank.append(record)

    result['rank'] = rank

    return result


# public tool 6
def get_all_cblock_user_key() -> list:
    result = []
    for block in Block_Chain:
        if block.get('index') == 0:
            continue
        user_key = block['proof']['userKey']
        result.append(user_key)
    return result


# public helper a
def get_BMC_helper(job: dict) -> json:
    global push_count
    uk = job.get('userKey')
    if not is_valid_user_key(uk):
        return get_BMC_error_reply()

    push_count += 1
    BMC = dict()
    BMC['result'] = True
    BMC['info'] = 'valid'
    block = get_latest_block()
    BMC['model'] = block
    BMC['userKey'] = uk
    pac = get_PAC()
    BMC['PAC'] = pac
    BMC['license'] = get_MD5_code(str(block) + pac)

    return json.dumps(BMC)


# public tool a
def get_PAC() -> str:
    push_token = 'BCMB-Push-' + str(push_count)
    return get_MD5_code(push_token)


# public tool (a, 2, 4, 5)
def is_valid_user_key(key: str) -> bool:
    if key in member['userKey'].values:
        return True
    else:
        return False


# socket serve space - start ###########################################################################################


# web serve space - start ###########################################################################################
def web_server():
    print('[INFO] BCMB Web Server Started...')
    app.run(host=HOST, port=1130)
    print('[Info] BCMB Web Server had been closed.')


# public helper router 5
@app.route('/bcmb/mycomment', methods=['GET', 'POST'])
def show_user_comment():
    if request.method == 'POST':
        uk = request.values['userKey']
        if not is_valid_user_key(uk):
            info = 'Invalid user key !'
            abort(403, info)
            return

        mi = member.query('userKey==@uk')
        pbk = request.values['publicKey']
        pvk = request.values['privateKey']

        if mi['publicKey'].values[0] == pbk and mi['privateKey'].values[0] == pvk:
            result = get_user_comment(uk)
            return result

        else:
            info = 'The public key or the private key is not matched with the user key.'
            abort(403, info)
            return
    elif request.method == 'GET':
        return 'Please use POST method to access.'


# public tool 5
def get_user_comment(user_key: str) -> json:
    result = dict()
    result['userKey'] = user_key
    result['lastUpdate'] = ''
    result['count'] = 0
    result['data'] = []

    comment_list = get_comment_list(user_key)
    if len(comment_list) > 0:
        result['lastUpdate'] = comment_list[-1]['timestamp']
        result['count'] = len(comment_list)
        data = []
        for comment in comment_list:
            record = dict()
            record['author'] = comment['author']
            record['comment'] = comment['comment']
            record['timestamp'] = comment['timestamp']
            data.append(record)

        result['data'] = data

    return json.dumps(result, indent=4)


# public tool 5
def get_comment_list(user_key: str) -> list:
    result = []
    for block in Block_Chain:
        if block['proof']['userKey'] == user_key:
            result.append(block)

    return result


# public helper router 7
@app.route('/bcmb')
def update_curr_chain():
    return get_curr_chain()


# public tool 7
def get_curr_chain() -> json:
    data = Block_Chain
    update_time = data[-1].get('timestamp')
    output = dict()
    output['lastUpdate'] = update_time
    output['data'] = data

    return json.dumps(output)


@app.route('/bcmb/lite')
def show_lite_comment():
    data = Block_Chain
    response = ''
    for block in data:
        if block['previous'] == '73}{ 93|\|35IZ o|= 8(|\/|8 O.-I9i|\|473|) \|/I7 _|37\/4`/|\|3':
            continue
        response += '<div>' + 'Author: ' + block['author'] + '</div>'
        response += '<br>'
        response += '<div>' + 'Comment: ' + block['comment'] + '</div>'
        response += '<br>'
        response += '<div>' + 'Push Time: ' + block['timestamp'] + '</div>'
        response += '<br>'
        response += '<div>' + 'User Key: ' + block['proof']['userKey'] + '</div>'
        response += '<br>'
        response += '<div>' + '———————————————————————————————————————————————————————————————————————————————————————' + '</div>'
        response += '<br>'

    if response == '':
        return 'No one has pushed comment.'

    return response


# web serve space - start ###########################################################################################

def main():
    init_BCMB()
    save_GB()
    try:
        task_web = threading.Thread(target=web_server, name='web')
        task_web.start()
        time.sleep(1)

        task_guard = threading.Thread(target=security_check, name='guard')
        task_guard.start()

        task_usher = threading.Thread(target=usher, name='usher')
        task_usher.start()

        task_serve = threading.Thread(target=serve, name='serve')
        task_serve.start()
    except Exception as e:
        print('[WARN] Main thread occurs error')
        print(e)

    task_dash_board = threading.Thread(target=dashboard, name='dashboard')
    task_dash_board.start()
    print('[INFO] Preparation complete.\n')


# public thread
def init_BCMB():
    global Block_Chain
    # the genesis of BCMB originated with JetVayne
    # '73}{ 93|\|35IZ o|= 8(|\/|8 O.-I9i|\|473|) \|/I7 _|37\/4`/|\|3'
    block = dict()
    block['previous'] = '73}{ 93|\|35IZ o|= 8(|\/|8 O.-I9i|\|473|) \|/I7 _|37\/4`/|\|3'
    block['index'] = 0
    block['author'] = 'Jet Vayne'
    block['comment'] = 'BCMC All rights reserved. Since 2019'
    block['timestamp'] = str(datetime.datetime.now())

    proof = dict()
    proof['userKey'] = 'BFC-Key'
    proof['nonce'] = 'void'
    proof['PAC'] = 'BFC-Key'
    proof['license'] = 'BFC-Key'
    block['proof'] = proof

    psv = dict()
    psv['signature'] = 'BCMB is initialed by Jet Vayne.'
    psv['publicKey'] = 'BFC-Key'
    block['PSV'] = psv

    Block_Chain.append(block)
    print('[INFO] BCMB Genesis Block has been initiated.')


# public thread
def save_GB():
    gen_block = Block_Chain[0]
    with open('genesis_block.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(gen_block, indent=4))
    print('[INFO] Finish backing up BCMB Genesis Block.')


# public thread stop tool
def stop_usher():
    global usher_flag
    usher_flag = False


# public thread stop tool
def stop_serve():
    global serve_flag
    serve_flag = False


# public thread stop tool
def stop_web_server():
    global serve_flag
    serve_flag = False


# public thread stop tool
def stop_dashboard():
    global da_flag
    da_flag = False


# public socket stop tool
def stop_socket_server():
    global s
    s.close()
    print('[Info] BCMB socket server has stopped.')


# public BCMB stop tool
def stop_BCMB_service():
    stop_socket_server()
    stop_usher()
    stop_serve()
    print('[INFO] BCMB Service has been suspend.')


# public secure thread
def security_check():
    global guard_flag
    print('[INFO] The chain guard is cruising...')
    while guard_flag:
        if not check_block():
            print('[WARN] The chain had been modified !!!')
            guard_flag = False
            stop_BCMB_service()


# public secure tool
def check_block():
    result = True
    for i, block in enumerate(Block_Chain):
        if i == 0 and not check_GB():
            return False

        if (i + 1) != len(Block_Chain):
            next_block = Block_Chain[i+1]

            hs = block.get('previous') + \
                 str(block.get('index')) + \
                 block.get('author') + \
                 block.get('comment') + \
                 block.get('timestamp') + \
                 block['proof'].get('userKey') + \
                 block['proof'].get('nonce') + \
                 block['proof'].get('PAC') + \
                 block['proof'].get('license') + \
                 block['PSV'].get('signature') + \
                 block['PSV'].get('publicKey') + \
                 next_block['proof']['userKey'] + next_block['proof']['nonce'] + next_block['comment']

            hash = hashlib.sha256()
            hash.update(hs.encode('utf-8'))
            check_hash = hash.hexdigest()
            if check_hash != next_block['previous']:
                return False

    return result


# public secure tool
def get_GB_data() -> dict:
    with open('genesis_block.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


# public secure tool
def check_GB():
    base = get_GB_data()
    curr = Block_Chain[0]
    if curr == base:
        return True
    else:
        return False


# public thread
def usher():
    global client_queue
    print('[INFO] Usher Service is started.')
    while usher_flag:
        try:
            client, address = s.accept()
            print('New Socket client:', address[0], '  address:', address[1])
            client.setblocking(False)
            client_queue.put(client)
        except:
            pass

    print('[INFO] TASK - usher finished.')


# public thread
def dashboard():
    print('[INFO] BCMB Dashboard is opened.')
    while da_flag:
        cmd = input()
        try:
            exec(cmd)
        except Exception as e:
            print(e)


# dashboard tool 1
def get_winner():
    all_block_keys = get_all_cblock_user_key()
    count_result = Counter(all_block_keys)
    if len(count_result) == 0:
        print('Can not choose a winner recently.')
        return
    else:
        rank = count_result.most_common(1)
        uk = rank[0][0]
        mi = member.query('userKey==@uk')
        name = mi['name'].values[0]
        print('The winners is ', name, '-', uk)
        print('Wanna check winner\'s lucky number? (y/n)')
        while True:
            cmd = input()
            if cmd == 'y':
                print(mi['luckyNum'].values[0])
                break
            elif cmd == 'n':
                break
            else:
                print('Error command code! Please retry.')


# dashboard tool 2
def sbc():
    with open('urgent_saved_chain.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(Block_Chain, indent=4))


if __name__ == '__main__':
    main()
