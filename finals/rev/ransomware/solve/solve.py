from scapy.all import *
from pwn import *

libc = ELF("./dist/libc.so.6")
context.binary = ELF("./dist/service")

packets = rdpcap("./dist/capture.pcapng")

pls = []
responses = []
for p in packets:
    pl = raw(p[TCP].payload)
    if pl:
        if p.dport == 1338:
            pls.append(pl)
        else:
            responses.append(pl)

libc.address = int(responses[1].split(b" ")[1],0) - 0x27c8a
rop_payload = pls[1][40+8+8:-1]
rop = ROP(libc)
for chunk in [rop_payload[x:x+8] for x in range(0, len(rop_payload), 8)]:
    val = u64(chunk)
    if val > 0x500000:
        print(rop.unresolve(val))
    else:
        print("value", hex(val))

stage1 = bytes([x ^ 42 for x in pls[3]])
e = ELF.from_bytes(stage1)
e.save("./solve/stage1")

from Crypto.Cipher import ChaCha20

cipher = ChaCha20.new(key=b"why does malware keep using rc4?", nonce=b"\0"*8)
stage2 = cipher.decrypt(pls[4][4:])

# binwalk stage2     
# DECIMAL       HEXADECIMAL     DESCRIPTION
# --------------------------------------------------------------------------------
# 264           0x108           ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)

def ror8(value, shift):
    """Perform a right rotation on an 8-byte value by 'shift' bits."""
    shift %= 64  # Ensure shift is within the range of 0-63
    return (value >> shift) | (value << (64 - shift)) & 0xFFFFFFFFFFFFFFFF

codes = [u64(stage2[x:x+8]) for x in range(0x88, 264, 8)]
imports = [u64(stage2[x:x+8]) for x in range(0x8,0x88, 8)]
stage2 = [x for x in stage2][264:]
out = []
for i in range(len(imports)):
    if codes[i] == 0:
        break
    real_addr = codes[i] ^ ror8(imports[i], 17)
    j = 0
    # Find the index in a1 where the value matches a2_code[i]
    while u64(bytes(stage2[j:j+8])) != codes[i]:
        j += 1
    out.append((j, rop.unresolve(real_addr)))
    

    # Perform the transformation and update a1
    stage2[j:j+8] = list(p64(0))

    # Update the subsequent bytes
    stage2[j + 8:j + 4+8] = [0x90]*4
for addr, name in sorted(out):
    print(hex(addr), name)

open("./solve/stage2", "wb").write(bytes(stage2))

# From find_time.c / wireshark capture
t = 1720325377
def test(sequence):
    source = open("./solve/solve.c", "r").read()
    source = source.replace("TIME", str(t))
    source = source.replace("CHOICES", sequence + "P"*(32-len(sequence)))
    with open("./solve/solve_tmp.c", "w") as f:
        f.write(source)
    os.system("gcc solve/solve_tmp.c -o solve/solve")
    return b64d(os.popen("./solve/solve | base64", "r").read())

def is_good(d):
    return d in [ord(x) for x in string.ascii_letters + string.digits + "_{}"]

def search(choice, i):
    if i == 32:
        print(choice)
        return test(choice)
    p = test(choice + "P")
    c = test(choice + "C")
    print(i)
    p_good = is_good(p[i])
    c_good = is_good(c[i])
    if not p_good and not c_good:
        return
    if p_good and not c_good:
        return search(choice + "P", i + 1)
    elif not p_good and c_good:
        return search(choice + "C", i + 1)
    else:
        choose_p = search(choice + "P", i + 1)
        if choose_p is None:
            return search(choice + "C", i + 1)
        return choose_p
        
print(search("", 0))