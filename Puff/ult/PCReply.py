import json


# push comment success reply
def get_PCS_reply() -> json:
    result = dict()
    result['result'] = True
    result['info'] = 'The submitted BCA was passed.'

    return json.dumps(result)


# push comment error reply
def get_PCE_reply_a() -> json:
    result = dict()
    result['result'] = False
    result['PCE'] = 'The user key is invalid.'

    return json.dumps(result)


def get_PCE_reply_b() -> json:
    result = dict()
    result['result'] = False
    result['PCE'] = 'The signature does not match with the publicKey.'

    return json.dumps(result)


def get_PCE_reply_c() -> json:
    result = dict()
    result['result'] = False
    result['PCE'] = 'The proof is invalid.'

    return json.dumps(result)


def get_PCE_reply_d() -> json:
    result = dict()
    result['result'] = False
    result['PCE'] = 'The main block chain had been changed.'

    return json.dumps(result)
