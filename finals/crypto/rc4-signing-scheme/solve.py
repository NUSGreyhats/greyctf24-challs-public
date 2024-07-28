import os
from pwn import *

HOST = "localhost"

p = remote(HOST, 32001)
def sign():
    p.sendlineafter(b">", b"1")
    return bytes.fromhex(p.recvline(keepends=False).decode())


# solution
def gen_js(key):
    S = bytearray(range(256))
    ret = []
    j = 0
    for i in range(256):
         j = (j + S[i] + key[i%len(key)])%256
         ret += [j]
         t = S[i]
         S[i] = S[j]
         S[j] = t
    return ret

def gen_key(js):
    S = bytearray(range(256))
    j = 0
    
    key = [0 for i in range(len(js))]
    
    for i in range(len(js)):

         key[i] = (js[i] - j - S[i]) % 256

         j = js[i]
         
         t = S[i]
         S[i] = S[j]
         S[j] = t

    return key

sig = sign()
iv, ct = sig[:128], sig[128:]
js = gen_js(iv)

for i in range(128):
    j = js[i]
    
    k = js[j]

    if i < j < k < 128 and all(x != i and x != j and x != k for x in js[i+1:j]):
        # swap (i,j), (j,k): (i,j,k) --> (j,i,k) --> (j,k,i)
        # swap (i,k), (j,i): (i,j,k) --> (k,j,i) --> (j,k,i)
        print(f"found triplet: ({i}, {j}, {k})")

        new_js = js[:128]
        new_js[i] = k
        new_js[j] = i
        new_iv = bytes(gen_key(new_js))

        p.sendlineafter(b">", b"2")
        p.sendlineafter(b":", (new_iv+ct).hex().encode())
        p.interactive()




