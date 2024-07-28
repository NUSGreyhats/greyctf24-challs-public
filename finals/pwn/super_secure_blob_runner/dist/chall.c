#include <stdlib.h>
#include <stdnoreturn.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdint.h>
#include <seccomp.h>


int check(char* code) {

	for (int i = 0; i < 0x1000; i += 1) {
		// block our syscall bytes the LAZY way:)
		if (code[i] == 0x0f || code[i] == 0x05 || code[i] == 0xcd || code[i] == 0x80)
			return 1;
	}

	// install seccomp filters as extra security!!
	// it shouldn't matter though, since syscall is blocked anyways
	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_KILL);
	if (!ctx)
		return 1;
	if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0) < 0)
		return 1;
	if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendfile), 0) < 0)
		return 1;
	if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0) < 0)
		return 1;
	seccomp_load(ctx);
	return 0;
}

void call_shellcode(char* code) {

	__asm__(
		".intel_syntax noprefix\n"
		"mov rax, rdi\n"
		"mov rsp, 0\n"
		"mov rbp, 0\n"
		"mov rbx, 0\n"
		"mov rcx, 0\n"
		"mov rdx, 0\n"
		"mov rdi, 0\n"
		"mov rsi, 0\n"
		"mov r8, 0\n"
		"mov r9, 0\n"
		"mov r10, 0\n"
		"mov r11, 0\n"
		"mov r12, 0\n"
		"mov r13, 0\n"
		"mov r14, 0\n"
		"mov r15, 0\n"
		"jmp rax\n"
		".att_syntax\n"
	);

}

int main() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);

	char* code = mmap((void*)0x13370000, 0x1000, 7, MAP_SHARED | MAP_ANONYMOUS, 0, 0);

	printf("Blob Runner> ");
	fgets(code, 0x1000, stdin);
	mprotect(code, 0x1000, 5);

	if (!check(code)) {
		call_shellcode(code);
	} else {
		printf("Bad Blob!\n");
	}
}
