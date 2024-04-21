from pwn import *
from gmpy2 import mpz, ceil
import gmpy2

from Crypto.Util.number import inverse

gmpy2.get_context().precision = int(5000)

p = 16288504871510480794324762135579703649765856535591342922567026227471362965149586884658054200933438380903297812918052138867605188042574409051996196359653039
q = (p - 1) // 2

query_g = 2
while True:
    if (pow(query_g, q, p) != 1):
        break
    query_g += 1

inv_2 = inverse(2, q)
n = 5

r = remote("localhost", int(9999))

r.recvuntil("g: ")
g = int(r.recvline().strip().decode())

r.recvuntil("mpk: ")
mpk = eval(r.recvline().strip().decode())

msk = []

for i in range(n):
    mrange = [0, q]
    k = mpz(0)
    for j in range(1, 600):
        t = pow(2, j, q)
        r.sendline("2")
        payload = [0] * n
        payload[i] = t
        r.sendline(" ".join(map(str, payload)))
        r.sendline(str(query_g))
        r.recvuntil("s_k:")
        sk = int(r.recvline().strip().decode())
        if (pow(sk, q, p) != 1):
            k += 1
        mrange[1] = min(mrange[1], ceil((k + 1) * q / (2 ** j)))
        mrange[0] = max(mrange[0], k * q // (2 ** j))
        k *= 2
    msk.append(mrange[0] + 1)

r.sendline("3")
r.recvuntil("g_r: ")
g_r = int(r.recvline().strip().decode())
r.recvuntil("c: ")
c = eval(r.recvline().strip().decode())

ans = []

for i in range(n):
    A = GF(p)(c[i] * inverse(pow(g_r, msk[i], p), p))
    b = GF(p)(g)
    ans.append(int(discrete_log(A, b, bounds=[0, 2^40 + 1], algorithm='lambda')))
               
r.sendline(" ".join(map(str, ans)))
r.interactive()
    
