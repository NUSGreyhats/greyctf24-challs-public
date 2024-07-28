from pwn import *

elf = ELF('./dist/chall')
key = elf.read(0x4010a0, 0x20)
enc = elf.read(0x404020, 40)

def RC4crypt(data, key):
    box_range = 256

    # slightly modified RC4 here
    # SBOX is reversed
    box = list(range(255, -1, -1))

    i = 0
    for j in range(box_range):
        i = (i + box[j] + (key[j % len(key)])) % box_range
        box[j], box[i] = box[i], box[j]

    i = j = 0
    out = []
    for c in data:
        i = (i + 1) % box_range
        j = (j + box[i]) % box_range
        box[i], box[j] = box[j], box[i]
        out.append((c ^ box[(box[i] + box[j]) % 256]))

    return out

# encrypt!
# enc = bytearray(RC4crypt(enc, b"grey{wasnt_that_fun_and_easy_XDXDXDXDXD}"))
# print([hex(i) for i in enc])
# for i in range(1, len(enc)):
#     enc[i] ^= enc[i-1]
# enc = xor(bytes(enc), 0x80)
#
# print(enc)
# print([i for i in enc])

dec = bytearray(xor(bytes(enc), 0x80))
for i in range(len(dec)-1, 0, -1):
    dec[i] ^= dec[i-1]
flag = "".join([chr(i) for i in RC4crypt(bytes(dec), key)])
print(flag)
