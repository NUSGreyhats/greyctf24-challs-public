from pwn import *

# HARDCODED CONSTANTS, REPLACE IF NECESSARY
# getchar GOT: 0x404040
# key: 0x405340
# enc_sc2: 0x405540

context.arch = "amd64"

key = bytes([0x44, 0x55, 0x62, 0x1d, 0x5d, 0x46, 0xf9, 0x2c, 0x32, 0x5e, 0x62, 0x5f, 0xb5, 0x95, 0xf6, 0x9e, 0x67, 0x4b, 0x3a, 0x29, 0x98, 0x0c, 0x12, 0x90, 0x19, 0xe8, 0xc1, 0xb4, 0xf7, 0xa6, 0x0b, 0x22])

sc = asm("""
// this blob of code is used to clean up the entire shellcode in program
c:
ret
b:
pop rbp
jmp c
a:
pop rax
jmp b
d:
rep movsb
// we need to turn our .TEXT back to r-x
mov rax, 0xa
and rdi, 0xfff000
mov rsi, 0x1000
mov rdx, 5
syscall
jmp a

start_hook_sc:
mov rax, rsp

// egg hunt on the stack to find the current level
find_level_stack:
    add rax, 4
    mov rbx, 0xdeadbeef
    xor ebx, [rax]
    cmp ebx, 0xd1beafe5
    jne find_level_stack

// TODO: change from 1 to 2
// check level == 1
mov ecx, [rax-4]
cmp ecx, 1
je level_2

mov rbx, 0xdeadbeefdeadbeef
jmp rbx

// decrypt next stage
// turn our code cave page writable once again
level_2:
push rax
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 7
syscall

decrypt_stage_2:
pop rax
// lol this r15 is only for later use
mov r15, 57
// ebx = KEY
mov dx, [rax-0x7]
mov rsi, 0xdeadbeef
xor rdx, rsi
xor rdx, rbx
mov rbx, rdx
shl edx, 5
add ebx, edx

// enc_sc2 --> HARDCODED!!!!!!!!!!!!!!!!!!!!!!!!!
mov rsi, 0x405540
xor rcx, rcx
// cx = size of enc_sc_2
mov cx, [rsi]
inc rsi
inc rsi

lea rdi, [rip]

// find the second occurrence of 0xbabe1337
// since the first occurrence is in this shellcode itself
mov r8, 2
wot:
dec r8

find_end:
    inc rdi
    mov edx, [rdi]
    cmp edx, 0xbabe1337
    jne find_end
    test r8, r8
    jne wot

// append enc_sc_2 to the end of our shellcode
push rdi
cld
push rcx
rep movsb
pop rcx
pop rdi
push rdi

mov rax, 0
mov rdx, 0
mov rsi, 0x405340

// xor patch loop
xor_loop:
    mov r8d, [rsi+rax]
    mov r9d, [rdi+rdx]
    xor r8d, r9d
    xor r8d, ebx
    mov [rdi+rdx], r8d

    add rax, 4
    add rdx, 4

    cmp rdx, rcx
    ja xor_loop_done

    // modulo again
    cmp rax, 32
    jne xor_loop

    mov rax, 0
    jmp xor_loop

// need to patch GOT once again
// need to patch jmp to getchar func
xor_loop_done:

// ???
lea rax, [rip-0x10]

find_getchar_loop:
    mov ebx, [rax]
    dec rax
    cmp ebx, 0xfceb5dc3
    jne find_getchar_loop

// this is hardcoded, RAX will be shellcode-1
// so the address of getchar is at $rax+0x4d
mov rbx, [rax+0x4f]
pop rdi

// patch getchar@got to point to sc2
// patch jmp in sc2 to jump to getchar
mov [rdi+2], rbx
mov rbx, 0x404040
mov [rbx], rdi

end:

// now, we clean up our enc sc 1!
lea rdi, [rip+a]
lea rcx, [rip+end]
sub rcx, rdi
dec rcx
mov byte ptr [rdi], 0
mov rsi, rdi
inc rdi
cld
rep movsb

// turn code cave unwritable!
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 5
syscall

.word 0x1337
.word 0xbabe
""")


# next stage shellcode
sc2 = asm("""
start_of_sc2:
// call getchar
mov rbx, 0xdeadbeefdeadbeef
call rbx
// DO NOT OVERWRITE RBX, RBX IS THE RETURN OF GETCHAR
mov rbx, rax
xor rdx, rdx

// switch case for WASD
cmp rax, 97
jb skip1
sub rax, 32
skip1:
cmp rax, 65
jz case_A
cmp rax, 87
jz case_W
cmp rax, 83
jz case_S
cmp rax, 68
jz case_D
jmp return_quietly 

// do the 2d array math!
case_W:
mov rdi, 1
sub r15, 18
jmp push_maze
case_A:
mov rdi, 2
sub r15, 1
jmp push_maze
case_S:
mov rdi, 3
add r15, 18
jmp push_maze
case_D:
mov rdi, 4
add r15, 1
jmp push_maze

// the real maze muahaha
push_maze:

movabs rcx, 0xffff
push rcx
movabs rcx, 0x00ffffff
push rcx
movabs rcx, 0xcff03c00
push rcx
movabs rcx, 0x3c300fff
push rcx
movabs rcx, 0xcffff00c
push rcx
movabs rcx, 0x0c033cf3
push rcx
movabs rcx, 0xcf30c03c
push rcx
movabs rcx, 0xf3cffffc
push rcx
movabs rcx, 0x00c03c0c
push rcx
movabs rcx, 0xfcf3cfcf
push rcx
movabs rcx, 0x0c3cdcff
push rcx
movabs rcx, 0xefccc303
push rcx
movabs rcx, 0xfc0f0303
push rcx
movabs rcx, 0xffffffff
push rcx

// we start checking whether we walked into a wall
mov rax, r15
mov rcx, 16
div ecx
nop
inc rax
mov r9, rax

// save value of rax into r10 for later use
mov r10, rax

// we do so by popping the corresponding values
pop_away:
pop r8
dec eax
test eax, eax
jne pop_away

// edx is the remainder(?)
// number of bits to shift
get_position:
shl edx, 1
neg edx
add edx, 30

// save value of rdx into r11 for later use
mov r11, rdx

test rdx, rdx
jz loop_shr_done

// we extract the bits that tell us whether it's a blank
loop_shr:
shr r8, 1
dec edx
test edx, edx
jnz loop_shr

loop_shr_done:
and r8, 3

// we restore the stack by popping the remaining maze values from the stack
restore_stack:
mov rax, r9
neg rax
add rax, 14

// pop off the rest of the maze from the stack
pop_remainder:
pop r9
dec eax
test eax, eax
jne pop_remainder

// we check if we walked into a wrong place
check_ded:
cmp r8, 2
jz do_win
test r8, r8
jnz final_cleanup

// we want to mark the spot as visited.
// we have to edit the push statements T_T pain
patch_hidden_maze:

// once again, we make the current page RWX
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 7
push r11
syscall
pop r11

// do our PATCH
// previously saved r10 and r11 is used here

mov rdi, 0x1
test r11, r11
jz loop_gen_or_mask_done

loop_gen_or_mask:
    shl rdi, 1
    dec r11
    test r11, r11
    jnz loop_gen_or_mask

loop_gen_or_mask_done:

// we calculate the address to patch
// this should be the same address that was used to identify our position
// in the maze
lea rsi, [rip+push_maze+0x83+0x3+11]
mov rcx, r10
xor r10, r10
mov rax, 11
mul rcx
sub rsi, rax

add rsi, 11
mov rdx, qword ptr [rsi]
or rdx, rdi
mov qword ptr [rsi], rdx

// make the page R-X
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 5
syscall

jmp return_quietly

// we won! now we decrypt everything and clean this place up
do_win:

lea rsi, [rsp-0x68]
mov rcx, 0
xor rax, rax
xor rdx, rdx
loop_get_key:
    mov rdx, [rsi+rcx*4]
    xor rax, rdx
    rol rax, 4
    inc rcx
    cmp rcx, 22
    jnz loop_get_key

push rax

mov rax, 0x404100
mov rdi, 0x4040c0
mov rcx, 43

loop_unxor_enc_flag:
    mov sil, byte ptr [rdi+rcx-1]
    mov dl, byte ptr [rax+rcx-1]
    xor sil, dl
    mov byte ptr [rdi+rcx-1], sil
    dec rcx
    test rcx, rcx
    jnz loop_unxor_enc_flag

pop rax

loop_unxor_enc_flag_2:
    xor qword ptr [rdi+rcx*8], rax
    inc rcx
    cmp rcx, 5
    jnz loop_unxor_enc_flag_2

push rax
and rax, 0xff
mov sil, byte ptr [rdi+rcx*8+0]
xor sil, al
mov byte ptr [rdi+rcx*8+0], sil

pop rax
shr rax, 8
push rax
and rax, 0xff

mov sil, byte ptr [rdi+rcx*8+1]
xor sil, al
mov byte ptr [rdi+rcx*8+1], sil

pop rax
shr rax, 8
and rax, 0xff
mov sil, byte ptr [rdi+rcx*8+2]
xor sil, al
mov byte ptr [rdi+rcx*8+2], sil

final_cleanup:

// once again, we make the current page RWX
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 7
syscall

// we clean our entire shellcode
lea rdi, [rip+start_of_sc2+2]
mov rsi, qword ptr [rdi]
mov rdx, 0x404040
mov qword ptr [rdx], rsi

dec rdi
dec rdi

lea rsi, [rip+cant_clean_this]
sub rsi, rdi
mov rcx, rsi
mov rsi, rdi
dec rdi
xchg rsi, rdi
cld

cant_clean_this:

rep movsb

// make the page R-X
lea rdi, [rip]
mov rsi, 0x1000
not rsi
inc rsi
and rdi, rsi

mov rax, 60
sub rax, 20
shr rax, 2
mov rsi, 0x1000
mov rdx, 5
syscall

return_quietly:
mov rax, rbx
ret
""")

enc_sc = xor(key, sc).hex()
enc_sc = struct.pack("<H", len(sc)).hex() + enc_sc
enc_sc_p = [enc_sc[i:i+2] for i in range(0, len(enc_sc), 2)]
print("char enc_sc[] = {0x" + ", 0x".join(enc_sc_p) + "};")

# print(sc2.hex())

enc_sc2 = xor(xor(sc2, key), b"\xad\x11\x75\xf1").hex()
enc_sc2 = struct.pack("<H", len(sc2)).hex() + enc_sc2
enc_sc2_p = [enc_sc2[i:i+2] for i in range(0, len(enc_sc2), 2)]
print("char enc_sc2[] = {0x" + ", 0x".join(enc_sc2_p) + "};")
# print(sc2.hex()[:8])
# print(key.hex()[:8])
print(hex(len(sc)))
print(hex(len(sc2)))


# print(hex(len(sc)))
# print(disasm(sc))
