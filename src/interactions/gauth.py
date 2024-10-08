import base64
import hashlib
import hmac
import struct
import time

# Code from https://stackoverflow.com/a/8549884, modified with typehints
def get_hotp_token(secret: str, intervals_no: int) -> str:
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return f"{h: 6}"

def get_totp_token(secret: str) -> str:
    return get_hotp_token(secret, intervals_no=int(time.time())//30)
