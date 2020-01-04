from Crypto.Hash import MD5


def get_MD5_code(token: str) -> str:
    result = MD5.new()
    result.update(token.encode('utf-8'))
    result = result.hexdigest()

    return result
