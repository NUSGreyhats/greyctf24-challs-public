from pwn import *
import hashlib

# this code is provided to solve the PROOF OF WORK on remote (to discourage brute-forcing)
def pow_solver(p):
    p.recvuntil(b"sha256(")
    challenge = p.recvuntil(b" + ", drop=True)
    p.recvuntil(b"(")
    difficulty = int(p.recvuntil(b")", drop=True))
    answer = 0
    log.info(f"finding pow for {challenge.decode()}, {difficulty}")
    while True:
        answer += 1
        h = hashlib.sha256()
        h.update(challenge + str(answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        if bits.startswith('0' * difficulty):
            break
    p.sendlineafter(b"answer: ", str(answer).encode())
    log.success("PoW solved!")

p = remote("localhost", 34568)

pow_solver(p) # uncomment if running on remote!

p.interactive()
