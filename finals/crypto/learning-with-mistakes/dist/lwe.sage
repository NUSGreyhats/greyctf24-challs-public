from secrets import randbits
from Crypto.Util.number import bytes_to_long, long_to_bytes
import numpy as np
from hashlib import sha512

n = 500
qbits = 32
mbits = 4
q = 2**qbits
F = GF(q)
x = F.gen()

def int_to_F(n):
    return sum(b*x**i for i,b in enumerate(map(int, bin(n)[2:][::-1])))

def F_to_int(f):
    return f.integer_representation()

def gen_key():
    return np.array([b for b in map(int, format(randbits(n), "0500b"))], dtype=object)

def gen_a():
    return np.array([int_to_F(randbits(qbits)) for _ in range(n)], dtype=object)

def gen_noise():
    return int_to_F(randbits(qbits - mbits))

def encrypt_mbits(m, s):
    a = gen_a()
    f = np.vectorize(F_to_int)
    m = int_to_F(m << (qbits - mbits))
    return (f(a), F_to_int(np.dot(a, s) + m + gen_noise()))

def decrypt_mbits(c, s):
    a,b = c
    f = np.vectorize(int_to_F)
    a,b = f(a), int_to_F(b)
    return F_to_int(b - np.dot(a,s)) >> (qbits - mbits)

def encrypt_m(m, s):
    m = bytes_to_long(m)
    c = []
    while m != 0:
        mb = m & 0b1111
        c.append(encrypt_mbits(mb, s))
        m >>= 4
    return c[::-1]

def decrypt_m(c, s):
    m = 0
    for cb in c:
        m <<= 4
        mb = decrypt_mbits(cb, s)
        m += int(mb)
    return long_to_bytes(m)


# https://www.daniellowengrub.com/blog/2024/01/03/fully-homomorphic-encryption
message = b"Original LWE use field GF(prime). TFHE use Mod(2^n). I use GF(2^n)"
key = gen_key()
ciphertext = encrypt_m(message, key)
assert decrypt_m(ciphertext, key) == message

flag = b"grey{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}"
keyhash = sha512(long_to_bytes(int(''.join(map(str, key)), 2))).digest()
flag_xored = bytes([a^^b for a,b in zip(flag, keyhash)]).hex()

print(ciphertext)
print(flag_xored)
# sage lwe.sage > log
