# BigNumber, mpmath package required
# run this before execute: pip install BigNumber mpmath

import random
from BigNumber import BigNumber

# https://www.delftstack.com/howto/python/python-generate-prime-number/
def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
            
    return prime_list

def make_keys(p: BigNumber, q: BigNumber):
    # place your own implementation of make_keys
    # use e = 65537 as if FIPS standard

    # p와 q의 곱을 구한 후 (p-1) * (q-1)의 곱 구하기
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # e는 주어진 값 65537로, d는 1로 초기 값 설정
    e = 65537
    d = 1

    # e와 곱해서 phi_n으로 나눴을 때 1이 되는 수가 d(개인 키)
    # e와 d 값이 같을 경우는 제외
    while e == d or (e * d) % phi_n != 1:
        d += 1

    return [e, d, n]

def rsa_encrypt(plain: BigNumber, e: BigNumber, n: BigNumber):
    # place your own implementation of rsa_encrypt
    # c = m^e mod N
    cipher = (plain ** e) % n

    return cipher

def rsa_decrypt(cipher: BigNumber, d: BigNumber, n: BigNumber):
    # place your own implementation of rsa_decrypt
    # m = c^d mod N
    plain = (cipher ** d) % n

    return plain

primes = primesInRange(100, 1000)

P = primes[random.randrange(0, len(primes))]
Q = primes[random.randrange(0, len(primes))]

while P == Q:
    P = primes[random.randrange(0, len(primes))]
    Q = primes[random.randrange(0, len(primes))]

M = random.randrange(2, 20)
e, d, N = make_keys(P, Q)
C = rsa_encrypt(M, e, N)
M2 = rsa_decrypt(C, d, N)

print(f"P = {P}, Q = {Q}, N = {N}, M = {M}, e = {e}, d = {d}, C = {C}, M2 = {M2}")

if M == M2:
    print("RSA Success!!")
else:
    print("RSA Failed...")
