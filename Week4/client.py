# ciphercommunicator client
# complete this program with your own AES-128-EBC implemetation.
# hint: Receiver.decrypt, encrypt_message

from socket import AddressFamily, SocketKind, socket
from threading import Thread

# for AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ENCRYPTION_KEY:bytes = b''
BLOCK_SIZE = 16

class Receiver(Thread):
    def __init__(self, socket:socket):
        super().__init__()
        self.socket = socket

    def decrypt(self, ciphertext:bytes) -> bytes:
        # place your own implementation of
        # AES-128-ECB decryption with pycryptodome

        # 복호화 진행하기 위한 AES 개체 생성
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)

        # 복호화 한 후 unpadding 진행
        plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

        return plaintext

    def handle_recv(self, received:bytes):
        try:
            decrypt_result = self.decrypt(received)
            print("Received: " + bytes.decode(decrypt_result, "UTF-8"))
        except:
            pass

    def run(self):
        while True:
            received:bytes = self.socket.recv(1024)
            self.handle_recv(received)

def encrypt_message(msg: bytes) -> bytes:
    # place your own implementation of
    # AES-128-ECB encryption with pycryptodome

    # 암호화 진행하기 위한 AES 개체 생성
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)

    # 인자 값 msg padding 진행 후 암호화 실행
    text = pad(msg, BLOCK_SIZE)
    ciphertext = cipher.encrypt(text)

    return ciphertext

client_socket = socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 24000))

print("[*] connected to 127.0.0.1:24000, Receiving an encryption key...")

# try to receive encryption key (128bits)
ENCRYPTION_KEY = client_socket.recv(16)
print("[*] Key received: " + str(ENCRYPTION_KEY))
print("[*] Now a chatting session is starting...")

# start receiving messages and chatting
Receiver(client_socket).start()

while True:
    msg = input("Message: ")
    msg_encoded = msg.encode("UTF-8")

    payload = encrypt_message(msg_encoded)
    client_socket.send(payload)
    
    print("Me: " + msg)
