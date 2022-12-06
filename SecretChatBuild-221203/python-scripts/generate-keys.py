from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

# 32바이트 (256비트) 랜덤 비밀키 생성
secret = Random.get_random_bytes(32)

# RSA 2048 키 생성 시작
rsa = RSA.generate(2048)
# 공개키 export
pubkey = rsa.public_key().export_key()
# 개인키 export
prikey = rsa.export_key()

print(encode_base64(secret) + '\n')

print(encode_base64(pubkey) + '\n')
print(encode_base64(prikey) + '\n')
