#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <wait.h>
#include <stdlib.h> 
#include <sys/shm.h> 
#include <string.h>
#include <time.h>

int main(){
    char buf[0x21];
    // TIME from find_time
    srand(TIME);
    int fd = open("./dist/flag.txt", O_RDONLY);
    read(fd, buf, 0x20);
    close(fd);
    char choices[] = "CHOICES";
    for(int i = 0; i < 0x20; i++){
        rand();
        buf[i] ^= rand()&0xff;
        if(choices[i] == 'P'){
            srand(rand());
        }
    }
    printf("%s\n", buf);
}