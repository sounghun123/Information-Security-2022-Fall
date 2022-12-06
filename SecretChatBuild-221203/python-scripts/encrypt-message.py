from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64

def decode_base64(b64):
    return base64.b64decode(b64)

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

def read_from_base64():
    return [ decode_base64(input()), input() ]

def pad_message(msg):
    # 메세지 패딩 구현
    padded_msg = pad(msg.encode('utf-8'), 16)

    return padded_msg

def encrypt_message(key, iv, msg):
    # AES 256 암호화 구현
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(msg)

    return encode_base64(ciphertext)

[secretkey, message] = read_from_base64()

message = pad_message(message)

# 16바이트 (128비트 IV 랜덤 생성)
randomiv = get_random_bytes(16)

randomiv_str = encode_base64(randomiv)
cipher_str = encrypt_message(secretkey, randomiv, message)

print(randomiv_str + '!' + cipher_str)