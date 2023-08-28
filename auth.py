import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGO = config("algo")

def token_response(token: str):
    return {"access_token": token}


def signJWT(uid: str):

    payload = {
        "uid": uid,
        "expires": time.time() + 3600 # 1hr
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return token_response(token)


def decodeJWT(token: str):
    # token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjaGFrcmFwYW5pQGdtYWlsLmNvbSIsImV4cGlyZXMiOjE2OTMyMjAxODAuMzAxMDc3fQ.4LFUzGhk06dGwiYM-pwwfIwSsxNaqrf4_pdLWZMLC14'
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
