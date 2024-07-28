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
    for(int j = 0; j < 200; j++){
        // 1720325376 from wireshark
        srand(1720325376+j);
        int fd = open("./dist/flag.txt", O_RDONLY);
        read(fd, buf, 0x20);
        close(fd);
        char choices[] = "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP";
        for(int i = 0; i < 0x20; i++){
            rand();
            buf[i] ^= rand()&0xff;
            if(choices[i] == 'P'){
                srand(rand());
            }
            // printf("%c\n", buf[i]);
        }
        if(buf[0] == 'g'){
            printf("%s\n", buf);
            printf("%ld\n", 1720325376+j);
        }
    }
}