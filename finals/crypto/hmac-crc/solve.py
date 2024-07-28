from pwn import *
import os

HOST = "localhost"

p = remote(HOST, 32000)

def encrypt(pt: bytes):
    p.sendlineafter(b">", b"1")
    p.sendlineafter(b":", pt.hex().encode())
    return bytes.fromhex(p.recvline().decode())

# Solution
D = [0 for i in range(129)]
for i in range(128):
    basis_vec = [0 for i in range(16)]

    idx = i//8
    bidx = (i%8)
    basis_vec[idx] |= 1<<bidx
    
    D[i] = encrypt(bytes(basis_vec))

D[128] = encrypt(bytes([0 for i in range(16)]))

xor = lambda a,b: bytes(x^y for x,y in zip(a,b))

def encrypt2(pt):
    ans = bytes([0 for i in range(32)])
    ct = 0
    for i in range(128):
        idx = i//8
        bidx = (i%8)
        if (pt[idx]>>bidx) & 1:
            ct += 1
            ans = xor(ans, D[i])
            
    if ct % 2 == 0:
        ans = xor(ans, D[128])
        
    return ans

p.sendlineafter(b">", b"2")
for _ in range(10):
    p.recvuntil(b"Encrypt ")
    chal = bytes.fromhex(p.recvline(keepends=False).decode())
    p.sendline(encrypt2(chal).hex().encode())
p.interactive()