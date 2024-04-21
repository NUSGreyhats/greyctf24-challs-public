from pwn import *


context.binary = e = ELF("./heapheapheap")

p = process()

def add(p, s, v):
    p.sendlineafter(b"Your choice: ", b"1")
    p.sendlineafter(b"Enter length", str(len(s) + 1).encode())
    p.sendlineafter(b"Enter string: ", s)
    p.sendlineafter(b"Enter value: ", str(v).encode())

def delete(p):
    p.sendlineafter(b"Your choice: ", b"3")
    p.recvuntil(b"The largest element is '")
    string = p.recvuntil(b"'")[:-1]
    p.recvuntil(b"with a value of ")
    return string, int(p.recvline())

if __name__ == '__main__':
    add(p, b"Heap", 5)
    add(p, b"I", 9)
    add(p, b"Hello, world", 10)
    add(p, b"Love", 8)
    add(p, b"!"*100, 1)

    print(delete(p)[0])
    print(delete(p)[0])
    print(delete(p)[0])
    print(delete(p)[0])
    print(delete(p)[0])

    p.interactive()
