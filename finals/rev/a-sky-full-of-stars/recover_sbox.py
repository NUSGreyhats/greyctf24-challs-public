from pwn import *


context.binary = ELF("./dist/stars")
context.log_level = "error"

out = {}
for i in range(pow(2,9)):
    tc = bytes([i&0xff, (i>>8)+2]+[0x41]*6)
    if any(not x for x in tc):
        continue
    p = process()
    p.sendline(tc)
    try:
        recv = p.recvline()
    except Exception as e:
        print("failed", tc)
        continue
    r = bytes.fromhex(recv.strip().decode())
    o = r[0] + ((r[1]&1)<<8)
    out[o] = i
    p.close()
print(out)
