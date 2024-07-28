import re


registers = [['rax', 'eax', 'ax', 'al'],
 ['rbx', 'ebx', 'bx', 'bl'],
 ['rcx', 'ecx', 'cx', 'cl'],
 ['rdx', 'edx', 'dx', 'dl'],
 ['rsi', 'esi', 'si', 'sil'],
 ['rdi', 'edi', 'di', 'dil'],
 ['rbp', 'ebp', 'bp', 'bpl'],
 ['rsp', 'esp', 'sp', 'spl'],
 ['r8', 'r8d', 'r8w', 'r8b'],
 ['r9', 'r9d', 'r9w', 'r9b'],
 ['r10', 'r10d', 'r10w', 'r10b'],
 ['r11', 'r11d', 'r11w', 'r11b'],
 ['r12', 'r12d', 'r12w', 'r12b'],
 ['r13', 'r13d', 'r13w', 'r13b'],
 ['r14', 'r14d', 'r14w', 'r14b'],
 ['r15', 'r15d', 'r15w', 'r15b']]
sizes = {"QWORD": 64, "DWORD": 32, "WORD": 16}

def get_r_size_register(reg: str)->str:
    for i in registers:
        if reg in i:
            return i[0]

    print(reg)
    raise Exception

def get_reg_size(reg: str):
    for i in registers:
        if reg in i:
            return [64 ,32, 16, 8][i.index(reg)]

def transform_mov(asm):
    result = []
    items = asm[4:].split(", ")
    has_deref = False
    size = None
    loc = None
    for i in range(len(items)):
        if re.match(r"(BYTE|.*?WORD) PTR .+\[r..\]", items[i]):
            has_deref=True
            size, _, loc = items[i].split()
            offset, reg = re.findall(r"(-?\d+|\w+)\[(.*?)\]", items[i])[0]
            is_src = i
        elif re.match(r"(BYTE|.*?WORD) PTR \[r.*?\]", items[i]):
            has_deref=True
            offset = None
            reg = re.findall(r"\[(.*?)\]", items[i])[0]
            size, _, loc = items[i].split()
            is_src = i

    if size:
        # INFO: source operand is a dereference
        if is_src:
            result.append(f"lea rsp, {offset}[{reg}]")
            reg = get_r_size_register(items[0])
            result.append(f"pop {reg}")

        # INFO: destination operand is a reference
        else:

            # if we want to save a QWORD, it is easy
            if size == "QWORD":
                result.append(f"lea rsp, {offset}+8[{reg}]")
                result.append(f"push {items[1]}")
            elif size == "DWORD":
                result.append(f"lea rsp, {offset}[{reg}]")
                result.append(f"pop r15")
                result.append("shr r15, 32")
                result.append("shl r15, 32")
                if items[1].isnumeric():
                    result.append(f"add r15, {items[1]}")
                    result.append(f"push r15")
                else:
                    reg = get_r_size_register(items[1])
                    result.append(f"shl {reg}, 32")
                    result.append(f"shr {reg}, 32")
                    result.append(f"add r15, {reg}")
                    result.append(f"push r15")
                # print(asm)
                # print("===")
                # print("\n".join(result))
                # print(size)
                pass
            elif size == "BYTE":
                if offset:
                    result.append(f"lea rsp, {offset}[{reg}]")
                else:
                    result.append(f"lea rsp, [{reg}]")
                result.append(f"pop r15")
                result.append("shr r15, 8")
                result.append("shl r15, 8")
                if items[1].isnumeric():
                    result.append(f"add r15, {items[1]}")
                    result.append(f"push r15")
                else:
                    reg = get_r_size_register(items[1])
                    result.append(f"shl {reg}, {64-8}")
                    result.append(f"shr {reg}, {64-8}")
                    result.append(f"add r15, {reg}")
                    result.append(f"push r15")
            else:
                raise Exception
                # print(items[1])


    else:
        # no dereferenced stuff
        result.append("lea rsp, scratch+8[rip]")
        for i in range(len(items)):
            if not items[i].isnumeric():
                orig_size = get_reg_size(items[i])
                items[i] = get_r_size_register(items[i])
        result.append(f"push {items[1]}")
        result.append(f"pop {items[0]}")
        if orig_size != 64:
            result.append(f"shl {items[0]}, {64-orig_size}")
            result.append(f"shr {items[0]}, {64-orig_size}")

    return result


def obfuscate(raw_asm: list) -> list:
    " takes in a list of instructions and emits list of obfuscated instructions "
    # we don't need function prologues in 2024 :D
    x = raw_asm.index("endbr64")
    raw_asm.pop(x)
    raw_asm[x] = "\n".join([i for i in """push rsp\n
pop rbx\n
push 0xfff\n
pop rdx\n
not rdx\n
and rbx, rdx\n
xor rsi, rsi\n
push rbx\npop rdi\n

retry:
sub rdi, 0x1000\n
push 21\npop rax\n
syscall\n
cmp al, 0xf2\n
jne retry\n

add rdi, 0x1000\n
push rdi\npop rbx\n
xor rdx, rdx\n

retry2:
add rdi, 0x1000\n
add rdx, 0x1000\n
push 21\npop rax
syscall\n
cmp al, 0xf2\n
jne retry2\n

// munmap stack
push 11\npop rax\n
push rbx\npop rdi\n
push rdx\npop rsi\n
syscall\n""".split("\n") if i])

    result = []
    for asm in raw_asm:
        if asm.startswith("mov\t"):
            result += transform_mov(asm)
        else:
            result.append(asm)
    return result


with open("./chall.s") as f:
    x = obfuscate([i.strip() for i in f.read().split("\n")])

with open("./chall.s", "w") as f:
    f.write("\n".join(x))

