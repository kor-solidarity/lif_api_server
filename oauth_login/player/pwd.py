from passlib.hash import hex_sha1

"""
뭐에 쓰이는 물건인고?
crypt_pass: 평문 암호화.
verify: 암호화된거 맞는지 확인. 근데 SHA1암호화체제 특성상 필요없을듯.
"""


def crypt_pass(password):
    """

    :param password:
    :return:
    """
    return hex_sha1.encrypt(password)


# devas redoni la rezulton.
def verify(hash_text, passwd):
    """
    :param hash_text: 암호
    :param passwd: 평문
    :return:
    """

    return hex_sha1.verify(passwd, hash_text)
