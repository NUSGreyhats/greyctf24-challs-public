#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <wait.h>
#include <sys/shm.h> 
#include <string.h>
#include <time.h>
#include <unistd.h>


void *mmap(void *, size_t,  int,  int,  int,  __off_t){
    asm("mov rax, 0x55f0da578c4bd81b");
    asm("mov rax, [rax]");
    asm("hlt");
}

void *memset(void *, int,  size_t){
    asm("mov rax, 0x5d511c2e110e5275");
    asm("mov rax, [rax]");
    asm("hlt");
}

int close(int){
    asm("mov rax, 0x1b2495a2efa68959");
    asm("mov rax, [rax]");
    asm("hlt");
}

ssize_t write(int fd, const void *buf, size_t count){
    asm("mov rax, 0x33b2517a86d9eb0b");
    asm("mov rax, [rax]");
    asm("hlt");
}


ssize_t read(int fd, void *buf, size_t count){
    asm("mov rax, 0x189066bd7d8d9bd");
    asm("mov rax, [rax]");
    asm("hlt");
}

int clock_gettime(clockid_t clk_id, struct timespec *tp){
    asm("mov rax, 0x175c1ec168423414");
    asm("mov rax, [rax]");
    asm("hlt");
}

void srand(unsigned int seed) {
    asm("mov rax, 0x7c8b0942031354ea");
    asm("mov rax, [rax]");
    asm("hlt");
}


int rand(){
    asm("mov rax, 0x14d5aa1600f3e5d9");
    asm("mov rax, [rax]");
    asm("hlt");
}

int open(const char *pathname, int flags){
    asm("mov rax, 0x7ab7e196eaadd041");
    asm("mov rax, [rax]");
    asm("hlt");
}

pid_t getpid(void){
    asm("mov rax, 0xa26aa4f03710cd6");
    asm("mov rax, [rax]");
    asm("hlt");
}

int usleep(useconds_t usec){
    asm("mov rax, 0x72d6344709a0fa67");
    asm("mov rax, [rax]");
    asm("hlt");
}

pid_t fork(void){
    asm("mov rax, 0x3981f34dfb76a55a");
    asm("mov rax, [rax]");
    asm("hlt");
}

pid_t wait(int*){
    asm("mov rax, 0x6d9e4b46db60dd1f");
    asm("mov rax, [rax]");
    asm("hlt");
}

void exit(int){
    asm("mov rax, 0x5cb96200dec27ed1");
    asm("mov rax, [rax]");
    asm("hlt");
}


void* shared_malloc(size_t size) {
  int prot = 3;
  int flags = 33;
  return mmap(NULL, size, prot, flags, -1, 0);
}


#define ROR(x,y) ((unsigned long)(x) >> (y) | (unsigned long)(x) << 64 - (y))


struct payload {
	int entry;
	int num_imports;
	unsigned long offsets[0x10];
	unsigned long codes[0x10];
	char data[];
};

void _start(char* section_start, struct payload *p){
    for(int i = 0; i < p->num_imports; i++){
		char *ptr = section_start;
		while(1){
			if(*(unsigned long*)ptr == p->codes[i]){
				*(unsigned long*)ptr = (ROR(p->offsets[i], 0x11)) ^ p->codes[i];
				ptr[8] = '\xff';
				ptr[9] = '\xd0';
				ptr[10] = '\x5d';
				ptr[11] = '\xc3';
				break;
			}
			ptr++;
		}
	}
    char buf[0x21];
    int fd = open("./flag.txt", 0);
    memset(buf, 0, 0x21);
    read(fd, buf, sizeof(buf)-1);
    close(fd);

    struct timespec t;

    clock_gettime(CLOCK_REALTIME, &t);

    srand(t.tv_sec);

    int n = 32;
    char *data = shared_malloc(n);

    int ppid = getpid();
    for(int i = 0; i < n; i++){
        int pid = fork();
        int k = rand() % 100;
        for(int j = 0; j<k;j++){
            usleep(1);
        }
        if(data[i]){
            break;
        }
        data[i] = rand()&0xff;
        if(pid) {
            srand(rand());
        }
    }
    int wpid;
    while ((wpid = wait(NULL)) > 0);
    if(ppid == getpid()){
        for(int i = 0; i<n; i++){
            buf[i] ^= data[i];
        }
    }
    fd = open("./flag.txt", 2 | 0100);
    write(fd, buf, sizeof(buf));
    close(fd);
    exit(0);
}