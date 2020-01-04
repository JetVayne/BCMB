import ecdsa
import json
from Crypto.Hash import MD5


# ult sign-up
def make_sign_up_reply(name: str, lucky_num: str, user_key: str, public_key: ecdsa.VerifyingKey,
                       private_key: ecdsa.SigningKey) -> json:
    reply = dict()
    reply['result'] = True
    reply['username'] = name
    reply['luckyNum'] = lucky_num
    reply['userKey'] = user_key
    reply['publicKey'] = str(public_key.to_pem(), encoding='utf-8')
    reply['privateKey'] = str(private_key.to_pem(), encoding='utf-8')

    return json.dumps(reply)


# ult sign-up
def create_user_key(username: str, lucky_num: str, public_key: ecdsa.VerifyingKey) -> str:
    uks = username + lucky_num + str(public_key.to_pem(), encoding='utf-8')
    result = MD5.new()
    result.update(uks.encode('utf-8'))
    result = result.hexdigest()

    return result
