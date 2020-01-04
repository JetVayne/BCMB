# coding: utf-8
import hashlib
import json
import requests
import socket
import sys
import ecdsa

from ult.tools import *
from ult.Intro import *
from ult.UserInput import *

VERSION = '1.2'
AST_NAME = 'Sherry'
FT_LIST = ['1', '2', '3', '4', '5', '6', '7', '8', 'q']

# HOST = 'ec2-34-234-194-147.compute-1.amazonaws.com'
HOST = 'localhost'
PORT = 7777
# SERVICE_5_URL = 'http://ec2-34-234-194-147.compute-1.amazonaws.com:1130/bcmb/mycomment'
SERVICE_5_URL = 'http://localhost:1130/bcmb/mycomment'
# SERVICE_7_URL = 'http://ec2-34-234-194-147.compute-1.amazonaws.com:1130/bcmb'
SERVICE_7_URL = 'http://localhost:1130/ bcmb'

is_login = False
login_name = ''

deploy_user_key = ''
deploy_private_key = None
deploy_public_key = None
DIFFICULTY = 5


# public thread
def use_service():
    first_intro(AST_NAME)
    service_flag = True
    while service_flag:
        cmd = input()
        if cmd not in FT_LIST:
            wrong_ft_intro_a()
            continue
        service_flag = False

        if cmd == '1':
            if is_login is False:

                print('Please decide a user name that you wanna called. (Or enter $b to leave.)')
                username = get_input_username()
                if username is None:
                    return recursive_serve()

                print('Please decide a lucky number that you like. (Or enter $b to leave.)')
                lucky_num = get_input_lucky_num()
                if lucky_num is None:
                    return recursive_serve()

                print('ok. Let me help you to sign up, please wait.')
                sign_up_service(username, lucky_num)
                return recursive_serve()

        elif cmd == '2':
            if is_login is False:

                print('No problem ! Just enter your user key. (Or enter $b to leave.)')
                siuk = get_input_siuk()
                if siuk is None:
                    return recursive_serve()

                print('Please enter the lucky number of the user key you typed just now. (Or enter $b to leave.)')
                siln = get_input_lucky_num()
                if siln is None:
                    return recursive_serve()

                sign_in_service(siuk, siln)
                return recursive_serve()

        elif cmd == '3':
            if is_login:
                check = set_keys_service()
                if check:
                    print('Finished setting keys.\n')
                    return recursive_serve()
                else:
                    print('Failed to set keys. Please make sure you have prepared all the key file.\n')
                    return recursive_serve()
            else:
                print('Failed to set keys, please sign in first!\n')
                return recursive_serve()

        elif cmd == '4':
            if is_login is False:
                print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                return recursive_serve()

        elif cmd == '5':
            if is_login is False:
                print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                return recursive_serve()

        elif cmd == '6':
            if is_login is False:
                print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                return recursive_serve()

        elif cmd == '7':
            print('OK. Let me show you all the comment on BCMB recently, please wait.\n')
            get_chain_service()
            return recursive_serve()

        elif cmd == '8':
            print('Hmm... maybe next time, I just want to chat with some hot AI now.\n')
            return recursive_serve()

        elif cmd == 'q':
            print('Bye, honey. See you ~')
            print('(I gotta go to veg.)')


# public thread
def recursive_serve():
    rs_intro(is_login, login_name, AST_NAME)
    if is_login:
        type_list = ['3', '4', '5', '6', '7', '8', 'q']
        service_flag = True
        while service_flag:
            cmd = input()
            # 防呆保護
            if cmd not in type_list:
                wrong_ft_intro_b()
                continue
            service_flag = False  # 防呆保護結束

            if cmd == '3':
                check = set_keys_service()
                if check:
                    print('Succeeded in setting keys.\n')
                    return recursive_serve()
                else:
                    print('Failed to set keys. Please make sure you have prepared all the key file.\n')
                    return recursive_serve()

            elif cmd == '4':
                if not has_set_key():
                    print('You have not set your key, please set !\n')
                    return recursive_serve()
                else:
                    print(
                        'Want to post some cool idea? Just write down the comment you wanna post. (Or enter $b to leave.)\n')
                    comment = get_input_comment()
                    if comment is None:
                        return recursive_serve()

                    print('Pushing comment takes some time and some luck, please wait for a while. :)')
                    push_comment_service(comment)
                    return recursive_serve()

            elif cmd == '5':
                if not has_set_key():
                    print('you have not set your key, please set !\n')
                    return recursive_serve()
                else:
                    print('Ok, let me check out for you, please wait.\n')
                    get_comment_service()
                    return recursive_serve()

            elif cmd == '6':
                if has_set_key():
                    print('No problem! Let me show you the rank of BCMB recently, please wait.\n')
                    get_rank_service()
                    return recursive_serve()
                else:
                    print('You have not set your key, please set !\n')
                    return recursive_serve()

            elif cmd == '7':
                print('No problem! Let me show you all the comment on BCMB recently, please wait.\n')
                get_chain_service()
                return recursive_serve()

            elif cmd == '8':
                print('Hmm... maybe next time, I am so tired now...\n')
                return recursive_serve()

            elif cmd == 'q':
                print('Ok. Bye, honey. See you ~')
                print('(Oh god, finally)')

    else:
        service_flag = True
        while service_flag:
            cmd = input()
            if cmd not in FT_LIST:
                wrong_ft_intro_a()
                continue
            service_flag = False

            if cmd == '1':
                if is_login is False:

                    print('Please decide a user name that you wanna called. (Or enter $b to leave.)')
                    username = get_input_username()
                    if username is None:
                        return recursive_serve()

                    print('Please decide a lucky number that you like. (Or enter $b to leave.)')
                    lucky_num = get_input_lucky_num()
                    if lucky_num is None:
                        return recursive_serve()

                    print('ok. Let me help you to sign up, please wait.')
                    sign_up_service(username, lucky_num)
                    return recursive_serve()

            elif cmd == '2':
                if is_login is False:

                    print('No problem ! Just enter your user key. (Or enter $b to leave.)')
                    siuk = get_input_siuk()
                    if siuk is None:
                        return recursive_serve()

                    print('Please enter the lucky number of the user key you typed just now. (Or enter $b to leave.)')
                    siln = get_input_lucky_num()
                    if siln is None:
                        return recursive_serve()

                    sign_in_service(siuk, siln)
                    return recursive_serve()

            elif cmd == '3':
                if is_login is False:
                    print('Failed to set keys. Please sign in first!\n')
                    return recursive_serve()

                check = set_keys_service()
                if check:
                    print('Succeeded in setting keys.\n')
                    return recursive_serve()
                else:
                    print('Failed to set keys. Please make sure you have prepared all the key file.\n')
                    return recursive_serve()

            elif cmd == '4':
                if is_login is False:
                    print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                    return recursive_serve()

            elif cmd == '5':
                if is_login is False:
                    print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                    return recursive_serve()

            elif cmd == '6':
                if is_login is False:
                    print('Sorry, I can\'t help you for doing that because you haven\'t signed in...\n')
                    return recursive_serve()

            elif cmd == '7':
                print('No problem! Let me show you all the comment on BCMB recently, please wait.\n')
                get_chain_service()
                return recursive_serve()

            elif cmd == '8':
                print('Hmm... maybe next time, I am so tired now...\n')
                return recursive_serve()

            elif cmd == 'q':
                print('Ok. Bye, honey. See you ~')
                print('(Oh god, finally)')


# public service 1
def sign_up_service(username, lucky_num):
    global is_login, login_name
    rd = dict()
    rd['service'] = '1'
    rd['username'] = username
    rd['luckyNum'] = lucky_num
    request = json.dumps(rd)

    response = None
    s = create_socket()
    try:
        s.connect((HOST, PORT))
        s.send(bytes(request, encoding="utf8"))
        response = s.recv(8192)
    except Exception as e:
        print(e)
        pass
    s.close()

    if response:
        response = json.loads(str(response, encoding='utf8'))
        if response.get('result') is True:
            print('Creating key-files...')
            create_key_files(response)
            print('Finished')
            print('Congratulations ' + username + ', you are successfully signed up.\n')
            print(response.get('userKey') + ' <- This is your user key.')
            print(
                'Please remember it or keep the user.pem file save, you can enter the user key to sign-in next time.\n')
            is_login = True
            login_name = username
        else:
            print('Sign up error occur.')
    else:
        print('Sign up error occur.')


# public service 2
def sign_in_service(input_uk: str, input_ln: str):
    global is_login, login_name
    rd = dict()
    rd['service'] = '2'
    rd['userKey'] = input_uk
    rd['luckyNum'] = input_ln
    request = json.dumps(rd)

    response = None
    s = create_socket()
    try:
        s.connect((HOST, PORT))
        s.send(bytes(request, encoding="utf8"))
        response = s.recv(8192)
    except Exception as e:
        # print(e)
        pass
    s.close()

    if response:
        response = json.loads(str(response, encoding='utf8'))
        if response.get('result'):
            is_login = True
            login_name = response.get('username')
            print('Dear ' + login_name + ', you have successfully signed in.\n')
            create_key_files(response)

        else:
            print('Oops, Failed to sign in. ' + response.get('SIE') + '\n')
    else:
        print('Failed to get Server response, please try again.\n')


# public service 3
def set_keys_service():
    result = True
    global deploy_user_key, deploy_public_key, deploy_private_key
    try:
        with open('user.pem') as f:
            deploy_user_key = f.read()
    except:
        print('oops, I can not find your user.pem file.')
        return False

    try:
        with open('public.pem') as f:
            deploy_public_key = ecdsa.VerifyingKey.from_pem(f.read())
    except:
        print('oops, I can not find your public.pem file.')
        return False

    try:
        with open('private.pem') as f:
            deploy_private_key = ecdsa.SigningKey.from_pem(f.read())
    except:
        print('oops, I can not find your public.pem file.')
        return False

    return result


# public imp 3
def has_set_key():
    if deploy_user_key != '' and deploy_public_key and deploy_private_key:
        return True
    else:
        return False


# public service 4
def push_comment_service(new_comment: str):
    BMC = get_BMC()
    if BMC is None:
        print('Failed to push comment. Can not get BMC from server.\n')
        return

    BMC = json.loads(BMC)
    if BMC.get('result') is False:
        print('Oh no, ' + BMC.get('info') + '\n')
        return

    latest_block = BMC.get('model')
    nonce = mine_nonce(latest_block, new_comment)
    if nonce == -1:
        print('Failed to push comment. Can not mine the nonce.\n')
        return
    print('Find possible nonce: ', str(nonce) + '\n')

    BCA = create_BCA(BMC, nonce, new_comment)
    request = json.dumps(BCA)

    response = None
    s = create_socket()
    try:
        s.connect((HOST, PORT))
        s.send(bytes(request, encoding="utf8"))
        response = s.recv(8192)
    except Exception as e:
        # print(e)
        pass
    s.close()

    if response:
        response = json.loads(str(response, encoding='utf8'))
        if response.get('result'):
            print(response.get('info'))
            print('Oh nice! Congratulations ' + login_name + ', your comment has been chained on BCMB.\n')
        else:
            print('Oh no, the pushing is failed.')
            print(response.get('PCE') + '\n')
    else:
        print('Failed to get Server response, please try again.\n')


# public imp 4
def create_BCA(BMC: dict, nonce: int, content: str) -> dict:
    bca = dict()
    bca['service'] = '4'
    bca['PAC'] = BMC.get('PAC')
    bca['license'] = BMC.get('license')
    bca['userKey'] = deploy_user_key
    bca['nonce'] = nonce
    bca['author'] = login_name
    bca['comment'] = content
    bca['publicKey'] = str(deploy_public_key.to_pem(), encoding='utf8')
    sig = deploy_private_key.sign(bytes(content, encoding='utf8'))
    bca['signature'] = sig.hex()

    return bca


# public imp 4
def mine_nonce(block: dict, new_comment: str) -> int:
    result = -1
    for nonce in range(sys.maxsize):
        if nonce % 50000 == 0:
            print('Mining...')

        temp_hash = get_x_hash(block, nonce, new_comment)
        if temp_hash[0:DIFFICULTY] == ''.join(['0'] * DIFFICULTY):
            result = nonce
            break

    return result


# public imp 4
def get_x_hash(block: dict, nonce: int, new_comment: str):
    hs = block.get('previous') + \
         str(block.get('index')) + \
         block.get('author') + \
         block.get('comment') + \
         block.get('timestamp') + \
         block['proof'].get('userKey') + \
         block['proof'].get('nonce') + \
         block['proof']['PAC'] + \
         block['proof']['license'] + \
         block['PSV']['signature'] + \
         block['PSV'].get('publicKey') + \
         deploy_user_key + str(nonce) + new_comment

    hash = hashlib.sha256()
    hash.update(hs.encode('utf-8'))
    result = hash.hexdigest()

    return result


# public service 5
def get_comment_service():
    url = SERVICE_5_URL
    rd = dict()
    rd['userKey'] = deploy_user_key
    rd['publicKey'] = deploy_public_key.to_pem()
    rd['privateKey'] = deploy_private_key.to_pem()

    res = requests.post(url, rd)
    if res.status_code == 200:
        res.encoding = 'utf8'
        response = json.loads(res.text, encoding='utf-8')
        print('You have pushed ' + str(response.get('count')) + ' comments.')
        save_comment(response)
        print('And your comment data has been saved as my_comment.json in your folder.\n')
    else:
        print(res.status_code)
        print(res.text)


# public service 6
def get_rank_service():
    rd = dict()
    rd['service'] = '6'
    rd['userKey'] = deploy_user_key
    request = json.dumps(rd)

    response = None
    s = create_socket()
    try:
        s.connect((HOST, PORT))
        s.send(bytes(request, encoding="utf8"))
        response = s.recv(8192)
    except Exception as e:
        print(e)
        pass
    s.close()

    if response:
        response = json.loads(str(response, encoding='utf8'))
        rank_result = response.get('rank')
        if len(rank_result) == 0:
            print('It seems that no one has pushed a comment on BCMB recently.')
            print('You should be the first one. :)\n')
        else:
            print('BCMB Rank - last updated at ' + response.get('lastUpdate') + ' :')
            for i in range(len(rank_result)):
                rank = rank_result[i]
                print(str(i + 1) + '. ', rank.get('username'), '-',
                      rank.get('userKey'), ':', rank.get('times'))

            print('Your rank : ' + response.get('userRank'))
            print()
    else:
        print('Failed to get Server response, please try again.\n')


# public service 7
def get_chain_service():
    url = SERVICE_7_URL
    res = requests.get(url)
    if res.status_code == 200:
        res.encoding = 'utf8'
        data = json.loads(res.text, encoding='utf8')
        print('Succeed in getting all comment on BCMB.')
        save_chain(data)
        print('And all the comment data has been saved as download_chain.json in your folder.\n')
    else:
        print('Failed to get Server response, please try again.\n')


# public service a
def get_BMC() -> dict:
    result = None
    rd = dict()
    rd['service'] = 'a'
    rd['userKey'] = deploy_user_key
    request = json.dumps(rd)

    response = None
    s = create_socket()
    try:
        s.connect((HOST, PORT))
        s.send(bytes(request, encoding="utf8"))
        response = s.recv(8192)
    except Exception as e:
        print(e)
        print('Failed to get the latest block model.')
        s.close()
        return result

    s.close()

    if response:
        result = json.loads(str(response, encoding='utf8'))
        return result

    return result


def awake():
    print('BCMB Client Service start.')
    print(AST_NAME, 'Version:', VERSION, '\n')
    use_service()


if __name__ == '__main__':
    awake()
