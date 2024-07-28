from pwn import *
import random
N = 50
base = 0x1337000

stuff = b""
# 8, 7, 9, then lookup tree
for j, k in enumerate([8, 7, 9]):
    for i in range(N):
        stuff += p64(base + (i+1+4 + j * (N+1))*8)
    stuff += p64(k)
stuff = p64(base + 4 * 8) + p64(base + (4 + N + 1)*8) + p64(base + (4 + (N + 1)*2)*8)+ p64(base + (4 + (N + 1)*3)*8) + stuff


out = [0]
sbox = list(range(512))
random.seed(267)
random.shuffle(sbox)
base2 = 0x1337000 + len(stuff)
def gen(depth, offset=0):
    global out
    if depth == 0:
        out += [sbox[offset]]
        out += [0]
    else:
        ridx = gen(depth - 1, offset + pow(2, depth - 1))
        lidx = gen(depth - 1, offset)
        out += [lidx*8 + base2, ridx*8 + base2]
    return len(out) - 2
idx_1 = gen(9)
out[0] = idx_1 * 8 + base2

stuff += b"".join(p64(x) for x in out)


assert len(stuff) < 0x10000

pollute_decls = "int a0 = 0;\n"
N2 = 255
for i in range(1, N2+1):
    pollute_decls += f"int {'*'*i}a{i} = &a{i-1};\n"


data = open("./stars.c", "r").read()
data = data.replace("OBFS_IDX", "("+"*"*N2 + "a"+str(N2)+")")
data = data.replace("(8)", f"({'*'*(N+1)}((int {'*'*(N+2)})mem)[0])")
data = data.replace("(7)", f"({'*'*(N+1)}((int {'*'*(N+2)})mem)[1])")
data = data.replace("(9)", f"({'*'*(N+1)}((int {'*'*(N+2)})mem)[2])")
data = data.replace("POLLUTE_DECLS", pollute_decls)
data = data.replace("STUFF_SIZE", str(len(stuff)))
data = data.replace("STUFF", "".join(["\\x"+hex(x ^ 42)[2:] for x in stuff]))

open("./stars-out.c", "w").write(data)
os.system("gcc stars-out.c -s -o stars")