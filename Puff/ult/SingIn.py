import json
import pandas as pd


# sign in success reply
def get_SIS_reply(data: pd.DataFrame, user_key: str, lucky_num: str) -> json:
    reply = dict()
    reply['result'] = True
    reply['username'] = data['name'].values[0]
    reply['luckyNum'] = lucky_num
    reply['userKey'] = user_key
    reply['publicKey'] = data['publicKey'].values[0]
    reply['privateKey'] = data['privateKey'].values[0]

    return json.dumps(reply)


# sign in error reply
def get_SIE_reply_a() -> json:
    reply = dict()
    reply['result'] = False
    reply['SIE'] = 'The submitted user key is invalid.'

    return json.dumps(reply)


def get_SIE_reply_b() -> json:
    reply = dict()
    reply['result'] = False
    reply['SIE'] = 'The submitted user key and lucky number is not matched.'

    return json.dumps(reply)
