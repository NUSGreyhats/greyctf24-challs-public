from pwn import *

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def mix_single_column(a):
    a[0], a[1], a[2], a[3] = a[1], a[2], a[3], a[0]

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

mapping = [[i * 4 + j for j in range(4)] for i in range(4)]

for i in range(1, 10):
    shift_rows(mapping)
    mix_columns(mapping)

shift_rows(mapping)

mapping = [mapping[i][j] for i in range(4) for j in range(4)]

r = remote("localhost", 35100)

m = b''
for i in range(256):
    m += bytes([i]) * 16

r.recvuntil("m:")
r.sendline(m.hex())
r.recvuntil("c: ")
c = r.recvline().strip().decode()
c = bytes.fromhex(c)
r.recvuntil("c_p: ")
c_p = r.recvline().strip().decode()
c_p = bytes.fromhex(c_p)

clist = [c[i:i+16] for i in range(0, len(c) - 16, 16)]

dec_map = [[-1 for _ in range(256)] for _ in range(256)]

for i in range(256):
    for j in range(16):
        dec_map[mapping[j]][clist[i][j]] = i

p = [0 for _ in range(16)]

for i in range(16):
    p[mapping[i]] = dec_map[mapping[i]][c_p[i]]

r.sendline(bytes(p).hex())

r.interactive()
