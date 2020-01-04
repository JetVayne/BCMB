import ecdsa


# ult PSV
def check_PSV(sig: str, pbk: str, comment: str) -> bool:
    check_pub_key = ecdsa.VerifyingKey.from_pem(pbk)
    check_sig = bytes.fromhex(sig)
    result = check_pub_key.verify(check_sig, bytes(comment, encoding='utf8'))

    return result
