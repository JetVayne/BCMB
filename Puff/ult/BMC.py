import json


# ult BMC
def get_BMC_error_reply() -> json:
    result = dict()
    result['result'] = False
    result['info'] = 'The user key is invalid.'

    return json.dumps(result)
