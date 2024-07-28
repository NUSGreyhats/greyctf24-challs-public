from pwn import *

sc = "xchg edi, esp;"
sc += "add esp, 0x520;"
sc += shellcraft.ptrace(0, 0)
sc += """
    cmp eax, -1
    jne worked
"""
sc += shellcraft.exit(0)
sc += """
worked:
"""
sc += "/* xor_key_1 --> edi */\n"
sc += shellcraft.gettimeofday(tv='esp')
sc += "mov edi, [esp]\n"
sc += "xor edi, [esp-0x20]\n"
sc += """
mov dword ptr [esp], 0x79657267
mov dword ptr [esp+4], 0x7b
"""
sc += shellcraft.write(1, 'esp', 5)
sc += "add esp, 0xac0"
sc += """
mov ecx, 8
loop:
xor [esp], edi
add esp, 4
sub ecx, 1
test ecx, ecx
jnz loop
sub esp, 4*8
"""
sc += shellcraft.write(1, 'esp', 32)
sc += "mov dword ptr [esp], 0x0a7d\n"
sc += shellcraft.write(1, 'esp', 2)
sc += shellcraft.exit(0)

contents = bytes(bytearray([i ^ 42 for i in asm(sc)]))
contents += b"\x00" * (0x1000-len(contents))

# encrypt flag
flag = b"tr1ppy_4ss_r3v3rs1ng_ch4ll3ngexd"
key =  int(0x7be61b4b).to_bytes(4, 'little')
enc = xor(key, flag)
contents = contents[:-len(enc)] + bytes([i ^ 42 for i in enc])

# write shellcode
with open("gate.bin", "wb") as f:
    f.write(contents)
