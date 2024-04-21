from Crypto.Util.number import getPrime, isPrime, inverse
from secrets import randbelow
from gmpy2 import mpz
from typing import List, Tuple

# References:
# https://eprint.iacr.org/2015/017.pdf

def generate_prime():
    while True:
        q = getPrime(512)
        p = 2 * q + 1
        if isPrime(p):
            return mpz(p), mpz(q)
        
def discrete_log_bound(a, g, bounds, p):
    cul = pow(g, bounds[0], p)
    for i in range(bounds[1] - bounds[0] + 1):
        if cul == a:
            return i + bounds[0]
        cul = (cul * g) % p
    raise Exception(f"Discrete log for {a} under base {g} not found in bounds ({bounds[0]}, {bounds[1]})")

class _FeDDH_MK:
    def __init__(self, g, n: int, p: int, q: int, mpk: List[int], msk: List[int]=None):
        self.g = g
        self.n = n
        self.p = p
        self.q = q
        self.msk = msk
        self.mpk = mpk

    def has_private_key(self) -> bool:
        return self.msk is not None

    def get_public_key(self):
        return _FeDDH_MK(self.g, self.n, self.p, self.q, self.mpk)
    
class _FeDDH_SK:
    def __init__(self, y: List[int], sk: int):
        self.y = y
        self.sk = sk

class _FeDDH_C:
    def __init__(self, g_r: int, c: List[int]):
        self.g_r = g_r
        self.c = c

    
class IPFE:
    @staticmethod
    def generate(n: int, prime: Tuple[int, int] = None):
        if (prime == None): p, q = generate_prime()
        else: p, q = prime
        g = mpz(randbelow(p) ** 2) % p
        msk = [randbelow(q) for _ in range(n)]
        mpk = [pow(g, msk[i], p) for i in range(n)]

        return _FeDDH_MK(g, n, p, q, mpk=mpk, msk=msk)

    @staticmethod
    def encrypt(x: List[int], pub: _FeDDH_MK) -> _FeDDH_C:
        if len(x) != pub.n:
            raise Exception("Encrypt vector must be of length n")
        
        r = randbelow(pub.q)
        g_r = pow(pub.g, r, pub.p)
        c = [(pow(pub.mpk[i], r, pub.p) * pow(pub.g, x[i], pub.p)) % pub.p for i in range(pub.n)]

        return _FeDDH_C(g_r, c)
    
    @staticmethod
    def decrypt(c: _FeDDH_C, pub: _FeDDH_MK, sk: _FeDDH_SK, bound: Tuple[int, int]) -> int:
        cul = 1
        for i in range(pub.n):
            cul = (cul * pow(c.c[i], sk.y[i], pub.p)) % pub.p
        cul = (cul * inverse(sk.sk, pub.p)) % pub.p
        return discrete_log_bound(cul, pub.g, bound, pub.p)
    
    @staticmethod
    def keygen(y: List[int], key: _FeDDH_MK, c: _FeDDH_C) -> _FeDDH_SK:
        if len(y) != key.n:
            raise Exception(f"Function vector must be of length {key.n}")
        if not key.has_private_key():
            raise Exception("Private key not found in master key")
        
        t = sum([key.msk[i] * y[i] for i in range(key.n)]) % key.q
        sk = pow(c.g_r, t, key.p)
        return _FeDDH_SK(y, sk)
    
if __name__ == "__main__":
    n = 10
    key = IPFE.generate(n)
    x = [i for i in range(n)]
    y = [i + 10 for i in range(n)]
    c = IPFE.encrypt(x, key)
    sk = IPFE.keygen(y, key, c)
    m = IPFE.decrypt(c, key.get_public_key(), sk, (0, 1000))
    expected = sum([a * b for a, b in zip(x, y)])
    assert m == expected
