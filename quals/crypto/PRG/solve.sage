from pwn import *
from param import A 

def bytes_to_bits(s):
    return list(map(int, ''.join(format(x, '08b') for x in s)))

remo = remote("localhost", int(35101))

F = PolynomialRing(GF(2), 192, 'x')

variables = F.gens()

r = vector(F, variables[64:128])
k = vector(F, variables[128:])

A = Matrix(F, A)

length = 10

for _ in range(100):
    x = vector(F, variables[:64])
    equations = []
    remo.recvuntil("Game ")
    remo.recvuntil("\n")
    remo.recvuntil("Output: ")
    output = bytes.fromhex(remo.recvuntil("\n").strip().decode())
    output = bytes_to_bits(output)
    for i in range(length * 8):
        t = 0
        for oo in range(64):
            t += x[oo]
        equations.append(t - output[i])
        if (i % 3 == 0): x = (A * x + r)
        if (i % 3 == 1): x = (A * x + k)
        if (i % 3 == 2): x = (A * x + r + k)

    equations = Ideal(equations).groebner_basis()
    if (len(equations) == 1):
        remo.sendline("0")
    else:
        remo.sendline("1")
    
