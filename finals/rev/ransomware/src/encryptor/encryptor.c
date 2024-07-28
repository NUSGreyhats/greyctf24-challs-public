#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <wait.h>
#include <stdlib.h> 
#include <sys/shm.h> 
#include <string.h>
#include <time.h>


void* shared_malloc(size_t size) {
  int prot = PROT_READ | PROT_WRITE;
  int flags = MAP_SHARED | MAP_ANONYMOUS;
  return mmap(NULL, size, prot, flags, -1, 0);
}


int main(){
    char buf[0x21];
    int fd = open("./flag.txt", O_RDONLY);
    memset(buf, 0, 0x21);
    read(fd, buf, sizeof(buf)-1);
    close(fd);

    struct timespec t;

    clock_gettime(CLOCK_REALTIME, &t);
    printf("%ld\n", t.tv_sec);
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
    fd = open("./flag.out", O_RDWR | O_CREAT);
    write(fd, buf, sizeof(buf));
    close(fd);
}