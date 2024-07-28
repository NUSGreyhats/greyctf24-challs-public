.file	"chall.c"
.intel_syntax noprefix
.text
.data
.type	prompt, @object
.size	prompt, 7
prompt:
.string	"\346\354\341\347\277\240"
.globl	n
.bss
.align 8
.type	n, @object
.size	n, 8
n:
.zero	8
.globl	str2
.align 8
.type	str2, @object
.size	str2, 8
str2:
.zero	8
.globl	i
.align 8
.type	i, @object
.size	i, 8
i:
.zero	8
.globl	sz
.align 4
.type	sz, @object
.size	sz, 4
sz:
.zero	4
.globl	tmp
.type	tmp, @object
.size	tmp, 1
tmp:
.zero	1
.globl	a
.align 8
.type	a, @object
.size	a, 8
a:
.zero	8
.globl	b
.align 8
.type	b, @object
.size	b, 8
b:
.zero	8
.data
.type	good, @object
.size	good, 7
good:
.string	"\356\351\343\345\241\212"
.type	flag_start, @object
.size	flag_start, 6
flag_start:
.string	"\347\362\345\371\373"
.globl	code
.bss
.align 4
.type	code, @object
.size	code, 4
code:
.zero	4
.globl	enc_flag
.data
.align 32
.type	enc_flag, @object
.size	enc_flag, 40
enc_flag:
.ascii	"\324\267t\023;\330.\323S\207\263q&$\271\001\210\341lh'\326\320"
.ascii	"P\020\265\033\244\326f\034w\305\246\311`\234T\007\371"
.globl	scratch
.bss
.align 8
.type	scratch, @object
.size	scratch, 8
scratch:
.zero	8
.globl	rnd
.align 4
.type	rnd, @object
.size	rnd, 4
rnd:
.zero	4
.data
.align 8
.type	bad, @object
.size	bad, 11
bad:
.string	"\356\357\364\240\356\351\343\345\241\212"
.globl	input
.bss
.align 32
.type	input, @object
.size	input, 256
input:
.zero	256
.globl	str
.align 8
.type	str, @object
.size	str, 8
str:
.zero	8
.globl	key
.align 8
.type	key, @object
.size	key, 8
key:
.zero	8
.globl	ptlen
.align 4
.type	ptlen, @object
.size	ptlen, 4
ptlen:
.zero	4
.globl	S
.align 32
.type	S, @object
.size	S, 256
S:
.zero	256
.globl	ct
.align 32
.type	ct, @object
.size	ct, 256
ct:
.zero	256
.globl	ciphertext
.align 8
.type	ciphertext, @object
.size	ciphertext, 8
ciphertext:
.zero	8
.globl	keylen
.align 4
.type	keylen, @object
.size	keylen, 4
keylen:
.zero	4
.globl	j
.align 4
.type	j, @object
.size	j, 4
j:
.zero	4
.globl	plaintext
.align 8
.type	plaintext, @object
.size	plaintext, 8
plaintext:
.zero	8
.text
.globl	_start
.type	_start, @function
_start:
.LFB9:
.cfi_startproc
push rsp
pop rbx
push 0xfff
pop rdx
not rdx
and rbx, rdx
xor rsi, rsi
push rbx
pop rdi
retry:
sub rdi, 0x1000
push 21
pop rax
syscall
cmp al, 0xf2
jne retry
add rdi, 0x1000
push rdi
pop rbx
xor rdx, rdx
retry2:
add rdi, 0x1000
add rdx, 0x1000
push 21
pop rax
syscall
cmp al, 0xf2
jne retry2
// munmap stack
push 11
pop rax
push rbx
pop rdi
push rdx
pop rsi
syscall
.cfi_def_cfa_offset 16
.cfi_offset 6, -16
lea rsp, scratch+8[rip]
push rsp
pop rbp
.cfi_def_cfa_register 6
lea	rcx, prompt[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L2
.L3:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L2:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L3
nop
lea rsp, i[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i+8[rip]
push 0
jmp	.L4
.L5:
lea rsp, str[rip]
pop rdx
lea rsp, i[rip]
pop rax
add	rax, rdx
movzx	eax, BYTE PTR [rax]
xor	eax, -128
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rax, 56
shr rax, 56
add r15, rax
push r15
lea	rax, tmp[rip]
lea rsp, scratch+8[rip]
push rax
pop rsi
lea rsp, scratch+8[rip]
push 1
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 1
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 1
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 49 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L4:
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L5
nop
lea	rax, input[rip]
lea rsp, str+8[rip]
push rax
lea rsp, scratch+8[rip]
push 0
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 0
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, str[rip]
pop rdx
lea rsp, scratch+8[rip]
push rdx
pop rsi
lea rsp, scratch+8[rip]
push 255
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 69 "chall.c" 1
syscall
# 0 "" 2
# 71 "chall.c" 1
lea rsp, [str]
pop rbx
lea rsp, [rbx+rax-1]
pop rcx
cmp cl, 0xa
jne not_newline
lea rsp, [rbx+rax-1]
pop rcx
shr rcx, 8
shl rcx, 8
push rcx
not_newline:

# 0 "" 2
#NO_APP
nop
lea	rcx, input[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L6
.L7:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L6:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L7
nop
lea rsp, i[rip]
pop rcx
lea rsp, ptlen[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i[rip]
pop rcx
cmp	rcx, 40
je	.L8
lea	rcx, bad[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L9
.L10:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L9:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L10
nop
lea rsp, i[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i+8[rip]
push 0
jmp	.L11
.L12:
lea rsp, str[rip]
pop rdx
lea rsp, i[rip]
pop rax
add	rax, rdx
movzx	eax, BYTE PTR [rax]
xor	eax, -128
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rax, 56
shr rax, 56
add r15, rax
push r15
lea	rax, tmp[rip]
lea rsp, scratch+8[rip]
push rax
pop rsi
lea rsp, scratch+8[rip]
push 1
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 1
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 1
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 49 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L11:
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L12
nop
lea rsp, code[rip]
pop r15
shr r15, 32
shl r15, 32
add r15, 1
push r15
lea rsp, code[rip]
pop rax
lea rsp, scratch+8[rip]
push rax
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 60
pop rax
shl rax, 32
shr rax, 32
#APP
# 56 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
nop
.L8:
lea	rcx, flag_start[rip]
lea rsp, str+8[rip]
push rcx
lea	rcx, input[rip]
lea rsp, str2+8[rip]
push rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
add r15, 5
push r15
lea rsp, i+8[rip]
push 0
jmp	.L13
.L15:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L13:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
lea rsp, str2[rip]
pop r9
lea rsp, i[rip]
pop r8
add	r8, r9
movzx	r8d, BYTE PTR [r8]
xor	r8d, -128
cmp	cl, r8b
jne	.L43
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L15
.L43:
nop
lea rsp, i[rip]
pop rcx
cmp	rcx, 5
je	.L16
lea	rcx, bad[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L17
.L18:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L17:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L18
nop
lea rsp, i[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i+8[rip]
push 0
jmp	.L19
.L20:
lea rsp, str[rip]
pop rdx
lea rsp, i[rip]
pop rax
add	rax, rdx
movzx	eax, BYTE PTR [rax]
xor	eax, -128
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rax, 56
shr rax, 56
add r15, rax
push r15
lea	rax, tmp[rip]
lea rsp, scratch+8[rip]
push rax
pop rsi
lea rsp, scratch+8[rip]
push 1
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 1
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 1
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 49 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L19:
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L20
nop
lea rsp, code[rip]
pop r15
shr r15, 32
shl r15, 32
add r15, 1
push r15
lea rsp, code[rip]
pop rax
lea rsp, scratch+8[rip]
push rax
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 60
pop rax
shl rax, 32
shr rax, 32
#APP
# 56 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
nop
.L16:
lea rsp, key+8[rip]
push 4198560
lea rsp, keylen[rip]
pop r15
shr r15, 32
shl r15, 32
add r15, 32
push r15
lea	rcx, input[rip]
lea rsp, plaintext+8[rip]
push rcx
lea	rcx, ct[rip]
lea rsp, ciphertext+8[rip]
push rcx
lea rsp, i+8[rip]
push 255
jmp	.L21
.L22:
lea rsp, i[rip]
pop rcx
lea rsp, scratch+8[rip]
push rcx
pop r8
shl r8, 32
shr r8, 32
lea rsp, i[rip]
pop rcx
lea rsp, scratch+8[rip]
push r8
pop r9
shl r9, 32
shr r9, 32
not	r9d
lea	r8, S[rip]
lea rsp, [rcx+r8]
pop r15
shr r15, 8
shl r15, 8
shl r9, 56
shr r9, 56
add r15, r9
push r15
lea rsp, i[rip]
pop rcx
sub	rcx, 1
lea rsp, i+8[rip]
push rcx
.L21:
lea rsp, i[rip]
pop rcx
test	rcx, rcx
jns	.L22
lea rsp, i+8[rip]
push 0
jmp	.L23
.L24:
lea rsp, -16+8[rbp]
push rdx
lea rsp, -8+8[rbp]
push rax
lea rsp, i[rip]
pop rcx
lea	r8, S[rip]
movzx	ecx, BYTE PTR [rcx+r8]
movzx	r8d, cl
lea rsp, j[rip]
pop rcx
lea	r10d, [r8+rcx]
lea rsp, key[rip]
pop r9
lea rsp, i[rip]
pop rcx
lea rsp, keylen[rip]
pop r8
movsx	r8, r8d
lea rsp, scratch+8[rip]
push rcx
pop rax
cqo
idiv	r8
lea rsp, scratch+8[rip]
push rdx
pop rcx
add	rcx, r9
movzx	ecx, BYTE PTR [rcx]
movsx	ecx, cl
add	ecx, r10d
movzx	ecx, cl
lea rsp, j[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i[rip]
pop rcx
lea	r8, S[rip]
add	rcx, r8
lea rsp, a+8[rip]
push rcx
lea rsp, j[rip]
pop rcx
lea rsp, scratch+8[rip]
push rcx
pop r8
shl r8, 32
shr r8, 32
lea	rcx, S[rip]
add	rcx, r8
lea rsp, b+8[rip]
push rcx
lea rsp, a[rip]
pop rcx
movzx	ecx, BYTE PTR [rcx]
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rcx, 56
shr rcx, 56
add r15, rcx
push r15
lea rsp, b[rip]
pop r8
lea rsp, a[rip]
pop rcx
movzx	r8d, BYTE PTR [r8]
lea rsp, [rcx]
pop r15
shr r15, 8
shl r15, 8
shl r8, 56
shr r8, 56
add r15, r8
push r15
lea rsp, b[rip]
pop rcx
movzx	r8d, BYTE PTR tmp[rip]
lea rsp, [rcx]
pop r15
shr r15, 8
shl r15, 8
shl r8, 56
shr r8, 56
add r15, r8
push r15
nop
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
lea rsp, -16[rbp]
pop rdx
lea rsp, -8[rbp]
pop rax
.L23:
lea rsp, i[rip]
pop rcx
cmp	rcx, 255
jle	.L24
nop
lea rsp, i+8[rip]
push 0
lea rsp, j[rip]
pop r15
shr r15, 32
shl r15, 32
add r15, 0
push r15
lea rsp, n+8[rip]
push 0
jmp	.L25
.L26:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, scratch+8[rip]
push rcx
pop r8
sar	r8, 63
shr	r8, 56
add	rcx, r8
movzx	ecx, cl
sub	rcx, r8
lea rsp, i+8[rip]
push rcx
lea rsp, i[rip]
pop rcx
lea	r8, S[rip]
movzx	ecx, BYTE PTR [rcx+r8]
movzx	r8d, cl
lea rsp, j[rip]
pop rcx
add	ecx, r8d
movzx	ecx, cl
lea rsp, j[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i[rip]
pop rcx
lea	r8, S[rip]
add	rcx, r8
lea rsp, a+8[rip]
push rcx
lea rsp, j[rip]
pop rcx
lea rsp, scratch+8[rip]
push rcx
pop r8
shl r8, 32
shr r8, 32
lea	rcx, S[rip]
add	rcx, r8
lea rsp, b+8[rip]
push rcx
lea rsp, a[rip]
pop rcx
movzx	ecx, BYTE PTR [rcx]
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rcx, 56
shr rcx, 56
add r15, rcx
push r15
lea rsp, b[rip]
pop r8
lea rsp, a[rip]
pop rcx
movzx	r8d, BYTE PTR [r8]
lea rsp, [rcx]
pop r15
shr r15, 8
shl r15, 8
shl r8, 56
shr r8, 56
add r15, r8
push r15
lea rsp, b[rip]
pop rcx
movzx	r8d, BYTE PTR tmp[rip]
lea rsp, [rcx]
pop r15
shr r15, 8
shl r15, 8
shl r8, 56
shr r8, 56
add r15, r8
push r15
nop
lea rsp, i[rip]
pop rcx
lea	r8, S[rip]
movzx	r8d, BYTE PTR [rcx+r8]
lea rsp, j[rip]
pop rcx
lea rsp, scratch+8[rip]
push rcx
pop r9
shl r9, 32
shr r9, 32
lea	rcx, S[rip]
movzx	ecx, BYTE PTR [r9+rcx]
add	ecx, r8d
movzx	ecx, cl
movsx	rcx, ecx
lea	r8, S[rip]
movzx	ecx, BYTE PTR [rcx+r8]
movzx	ecx, cl
lea rsp, rnd[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, plaintext[rip]
pop r8
lea rsp, n[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
lea rsp, scratch+8[rip]
push rcx
pop r8
shl r8, 32
shr r8, 32
lea rsp, rnd[rip]
pop rcx
lea rsp, scratch+8[rip]
push r8
pop r9
shl r9, 32
shr r9, 32
xor	r9d, ecx
lea rsp, ciphertext[rip]
pop r8
lea rsp, n[rip]
pop rcx
add	rcx, r8
lea rsp, scratch+8[rip]
push r9
pop r8
shl r8, 32
shr r8, 32
lea rsp, [rcx]
pop r15
shr r15, 8
shl r15, 8
shl r8, 56
shr r8, 56
add r15, r8
push r15
lea rsp, n[rip]
pop rcx
add	rcx, 1
lea rsp, n+8[rip]
push rcx
.L25:
lea rsp, ptlen[rip]
pop rcx
movsx	r8, ecx
lea rsp, n[rip]
pop rcx
cmp	r8, rcx
ja	.L26
nop
nop
lea rsp, i+8[rip]
push 1
jmp	.L27
.L28:
lea rsp, i[rip]
pop rcx
lea	r8, ct[rip]
movzx	r9d, BYTE PTR [rcx+r8]
lea rsp, i[rip]
pop rcx
lea	r8, -1[rcx]
lea	rcx, ct[rip]
movzx	r8d, BYTE PTR [r8+rcx]
lea rsp, i[rip]
pop rcx
xor	r9d, r8d
lea	r8, ct[rip]
lea rsp, [rcx+r8]
pop r15
shr r15, 8
shl r15, 8
shl r9, 56
shr r9, 56
add r15, r9
push r15
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L27:
lea rsp, ptlen[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L28
lea rsp, ptlen[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea	rcx, enc_flag[rip]
lea rsp, str+8[rip]
push rcx
lea	rcx, ct[rip]
lea rsp, str2+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L29
.L31:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L29:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
lea rsp, str2[rip]
pop r9
lea rsp, i[rip]
pop r8
add	r8, r9
movzx	r8d, BYTE PTR [r8]
xor	r8d, -128
cmp	cl, r8b
jne	.L44
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L31
.L44:
nop
lea rsp, ptlen[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jne	.L32
lea	rcx, good[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L33
.L34:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L33:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L34
nop
lea rsp, i[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i+8[rip]
push 0
jmp	.L35
.L36:
lea rsp, str[rip]
pop rdx
lea rsp, i[rip]
pop rax
add	rax, rdx
movzx	eax, BYTE PTR [rax]
xor	eax, -128
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rax, 56
shr rax, 56
add r15, rax
push r15
lea	rax, tmp[rip]
lea rsp, scratch+8[rip]
push rax
pop rsi
lea rsp, scratch+8[rip]
push 1
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 1
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 1
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 49 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L35:
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L36
nop
lea rsp, code[rip]
pop rax
lea rsp, scratch+8[rip]
push rax
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 60
pop rax
shl rax, 32
shr rax, 32
#APP
# 56 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
nop
.L32:
lea	rcx, bad[rip]
lea rsp, str+8[rip]
push rcx
lea rsp, i+8[rip]
push 0
jmp	.L37
.L38:
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L37:
lea rsp, str[rip]
pop r8
lea rsp, i[rip]
pop rcx
add	rcx, r8
movzx	ecx, BYTE PTR [rcx]
test	cl, cl
jne	.L38
nop
lea rsp, i[rip]
pop rcx
lea rsp, sz[rip]
pop r15
shr r15, 32
shl r15, 32
shl rcx, 32
shr rcx, 32
add r15, rcx
push r15
lea rsp, i+8[rip]
push 0
jmp	.L39
.L40:
lea rsp, str[rip]
pop rdx
lea rsp, i[rip]
pop rax
add	rax, rdx
movzx	eax, BYTE PTR [rax]
xor	eax, -128
lea rsp, tmp[rip]
pop r15
shr r15, 8
shl r15, 8
shl rax, 56
shr rax, 56
add r15, rax
push r15
lea	rax, tmp[rip]
lea rsp, scratch+8[rip]
push rax
pop rsi
lea rsp, scratch+8[rip]
push 1
pop rax
shl rax, 32
shr rax, 32
lea rsp, scratch+8[rip]
push 1
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 1
pop rdx
shl rdx, 32
shr rdx, 32
#APP
# 49 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
lea rsp, i[rip]
pop rcx
add	rcx, 1
lea rsp, i+8[rip]
push rcx
.L39:
lea rsp, sz[rip]
pop rcx
movsx	r8, ecx
lea rsp, i[rip]
pop rcx
cmp	r8, rcx
jg	.L40
nop
lea rsp, code[rip]
pop rax
lea rsp, scratch+8[rip]
push rax
pop rdi
shl rdi, 32
shr rdi, 32
lea rsp, scratch+8[rip]
push 60
pop rax
shl rax, 32
shr rax, 32
#APP
# 56 "chall.c" 1
syscall
# 0 "" 2
#NO_APP
nop
nop
pop	rbp
.cfi_def_cfa 7, 8
ret
.cfi_endproc
.LFE9:
.size	_start, .-_start
.ident	"GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
.section	.note.GNU-stack,"",@progbits
.section	.note.gnu.property,"a"
.align 8
.long	1f - 0f
.long	4f - 1f
.long	5
0:
.string	"GNU"
1:
.align 8
.long	0xc0000002
.long	3f - 2f
2:
.long	0x3
3:
.align 8
4:
