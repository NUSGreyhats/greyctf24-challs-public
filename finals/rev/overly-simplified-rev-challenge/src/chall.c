#include <syscall.h>
#include <unistd.h>

register int    rdx asm("rdx");
static char prompt[] = "\xe6\xec\xe1\xe7\xbf\xa0"; // flag? 
register int    rax asm("rax");
register int    rdi asm("rdi");
size_t n;
char* str2;
register char*  rsi asm("rsi");
long i;
int sz;
unsigned char tmp;
unsigned char* a;
unsigned char* b;
static char good[] = "\xee\xe9\xe3\xe5\xa1\x8a"; // nice!\n
static char flag_start[] = "\xe7\xf2\xe5\xf9\xfb";
int code = 0;
char enc_flag[] = {212, 183, 116, 19, 59, 216, 46, 211, 83, 135, 179, 113, 38, 36, 185, 1, 136, 225, 108, 104, 39, 214, 208, 80, 16, 181, 27, 164, 214, 102, 28, 119, 197, 166, 201, 96, 156, 84, 7, 249};
long long scratch = 0;
int rnd;
static char bad[] = "\xee\xef\xf4\xa0\xee\xe9\xe3\xe5\xa1\x8a"; // not nice!\n
char input[0x100] = {0};
char* str;
char *key;
int ptlen;
unsigned char S[256];
char ct[0x100] = {0};
unsigned char* ciphertext;
int keylen;
unsigned int j;
unsigned char* plaintext;


inline void __attribute__((always_inline)) _strlen() {
	for (i = 0; str[i] != 0; i++) {}
}

inline void __attribute__((always_inline)) _write() {
// void _write() {
	_strlen();
	sz = i;
	for (i = 0; i < sz; i++) {
		tmp = *(str+i) ^ 0x80;
		rsi = &tmp;
		rax = SYS_write;
		rdi = 1;
		rdx = 1;
		asm("syscall");
	}
}

inline void __attribute__((always_inline)) my_exit() {
	rdi = code;
	rax = SYS_exit;
	asm("syscall");
}

inline void __attribute__((always_inline)) _strcmp() {
// void _strcmp() {
	for (i = 0; ((unsigned char)str[i] == (unsigned char)(str2[i]^0x80)) && (i < sz); i++);
}

inline void __attribute__((always_inline)) _read_to_str() {
	rax = SYS_read;
	rdi = 0;
	rsi = str;
	rdx = 0xff;
	asm("syscall");
	// trim newline
	__asm__(
		"lea rsp, [str]\n"
		"pop rbx\n"
		"lea rsp, [rbx+rax-1]\n"
		"pop rcx\n"
		"cmp cl, 0xa\n"
		"jne not_newline\n"

		"lea rsp, [rbx+rax-1]\n"
		"pop rcx\n"
		"shr rcx, 8\nshl rcx, 8\n"
		"push rcx\n"
		"not_newline:\n"
	);
}

inline void __attribute__((always_inline)) swap() {
// void swap() {
	a = &S[i];
	b = &S[j];
    tmp = *a;
    *a = *b;
    *b = tmp;
}

inline void __attribute__((always_inline)) KSA() {
// void KSA() {
	for (i = 255; i >= 0; i--) {
		S[i] = 255-i;
	}

	for (i = 0; i < 256; i++) {
		j = (j + S[i] + key[i % keylen]) % 256;
		swap();
	}
}

inline void __attribute__((always_inline)) PRGA() {
// void PRGA() {
	i = 0;
	j = 0;

	for(n = 0;  n < ptlen; n++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;

        swap();
        rnd = S[(S[i] + S[j]) % 256];

        ciphertext[n] = rnd ^ plaintext[n];

    }
}

inline void __attribute__((always_inline)) RC4() {
// void RC4() {
    KSA();
    PRGA();
}

void _start() {

	// print prompt
	str = prompt;
	_write();

	// get input
	str = input;
	_read_to_str();

	// 1. check length == 33
	str = input;
	_strlen();
	ptlen = i;

	if (i != 40) {
		str = bad;
		_write();
		code = 1;
		my_exit();
	}

	// 2. check correct flag header
	str = flag_start;
	str2 = input;
	sz = 5;
	_strcmp();

	if (i != 5) {
		str = bad;
		_write();
		code = 1;
		my_exit();
	}

	// 3. we want to do rc4 :3
	key = (char*)0x4010a0;
	keylen = 0x20;
	plaintext = input;
	ciphertext = ct;
	RC4();

	for (i = 1; i < ptlen; i++) {
		ct[i] ^= ct[i-1];
	}

	sz = ptlen;
	str = enc_flag;
	str2 = ct;
	_strcmp();
	
	if (i == ptlen) {
		// 4. flag is correct!
		str = good;
		_write();
		my_exit();
	}

	str = bad;
	_write();
	my_exit();
}
