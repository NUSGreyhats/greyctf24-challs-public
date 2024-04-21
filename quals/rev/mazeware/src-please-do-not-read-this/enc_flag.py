from Crypto.Cipher import ARC4
from pwn import xor, p64

def b_to_c_arr(b: bytes) -> str:
    a = b.hex()
    b = [a[i:i+2] for i in range(0, len(a), 2)]
    return "{0x" + ", 0x".join(b) + "}"


FLAG        = b"grey{h1dd3n_1n_pl41n51gh7_35ffcbede152a94e}"
FAKE_FLAG   = b"https://www.youtube.com/watch?v=dQw4w9WgXcQ"
KEY = bytearray([0x44, 0x55, 0x62, 0x1d, 0x5d, 0x46, 0xf9, 0x2c, 0x32, 0x5e, 0x62, 0x5f, 0xb5, 0x95, 0xf6, 0x9e, 0x67, 0x4b, 0x3a, 0x29, 0x98, 0x0c, 0x12, 0x90, 0x19, 0xe8, 0xc1, 0xb4, 0xf7, 0xa6, 0x0b, 0x22])

a = ARC4.new(KEY).encrypt(FLAG)
b = ARC4.new(KEY).encrypt(FAKE_FLAG)
c = xor(xor(a, b), p64(0xdf07b7a75dac852d))
d = xor(b, c)
# d = xor(KEY, )
# c = xor(a, p64(0xdf07b7a75dac852d))
#
assert len(a) == len(b) == len(c)

print(len(a))
print(b_to_c_arr(a))
print(b_to_c_arr(b))
print(b_to_c_arr(c))
print(b_to_c_arr(d))
