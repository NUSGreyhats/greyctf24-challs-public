import functools 
import binascii
from gmpy2 import mpz
from tqdm import tqdm


FLAG = b"grey{ea_sports_its_in_the_game_586256cbd58140ec}"

p = mpz(2933342412243178360246913963653176924656287769470170577218737)
q = mpz(2663862733012296707089609302317500558193537358171126836499053)
m = p * q
e = 65537
phi = (p-1)*(q-1)

d = pow(65537, -1, phi)

def n_to_bs(n):
    bs = [0] * 64
    i = 63
    while n > 0:
        bs[i] = int(n & 0xff)       # cast to int from mpz
        n = n >> 8
        i -= 1
    return bs

def transform(bs, wave):
    if len(bs) < 64:
        bs = [0] * (64-len(bs)) + bs

    # xor
    k = wave & 0xff
    for i in range(24, len(bs)):
        k_ = bs[i]
        bs[i] = bs[i] ^ k
        k = k_

    # scrambling
    for i in range(24, len(bs)):
        ti = ((i * wave) % 40) + 24
        bs[ti], bs[i] = bs[i], bs[ti]

    # rsa
    n = mpz(functools.reduce(lambda a, b: (a << 8) + b, bs, 0))
    n = pow(n, d, m)
    bs = n_to_bs(n)

    return bs

def untransform(bs, wave):
    if len(bs) < 64:
        bs = [0] * (64-len(bs)) + bs

    # rsa
    n = mpz(functools.reduce(lambda a, b: (a << 8) + b, bs, 0))
    n = pow(n, e, m)
    bs = n_to_bs(n)

    # scrambling
    for i in range(len(bs)-1, 23, -1):
        ti = ((i * wave) % 40) + 24
        bs[i], bs[ti] = bs[ti], bs[i]

    # xor
    k = wave & 0xff
    for i in range(24, len(bs)):
        bs[i] = bs[i] ^ k
        k = bs[i]

    return bs

GGWAVE = 10000000

# t = list(FLAG)
# for i in tqdm(range(GGWAVE, 0, -1)):
#     t = transform(t, i)
# print(t)

t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 196, 180, 45, 13, 53, 112, 133, 142, 221, 121, 3, 157, 113, 81, 80, 195, 253, 225, 197, 202, 197, 48, 46, 21, 121, 40, 23, 239, 35, 175, 254, 103, 36, 126, 183, 218, 112, 235, 9, 98, 99, 29, 109, 196, 120, 43, 68, 126, 100, 81]

for i in tqdm(range(GGWAVE)):
    t = untransform(t, i+1)
print(t)
print(bytes(t)[16:])
