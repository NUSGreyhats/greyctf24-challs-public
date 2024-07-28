#define _GNU_SOURCE   
#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>
#include <string.h>

void load(int *****e, int ****d){
    *e = d;
}

int main(){

    void *mem = mmap((void*)0x1337000LL, 0x10000, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    memcpy(mem, "STUFF", STUFF_SIZE);
    memfrob(mem, STUFF_SIZE);


    char *buf = NULL;
    size_t len = 0;
    getline(&buf, &len, stdin);
    size_t blen = strlen(buf) * (8);
    if(blen % (9) != 0){
        exit(-1);
    }
    unsigned char *out = calloc(1, strlen(buf)+2);
    size_t ptr_idx = 0;
    size_t write_idx = 0;
    int **********ptr = *((int ************)mem)[3];
    int *********ptr1;
    int ********ptr2;
    int *******ptr3;
    int ******ptr4;
    int *****ptr5;
    int ****ptr6;
    int ***ptr7;
    int **ptr8;
    int *ptr9;

    POLLUTE_DECLS

    while(OBFS_IDX < blen){
        if(buf[OBFS_IDX/(8)] & (1<<(OBFS_IDX % (8)))){
            if(ptr_idx == 0){
                ptr1 = ptr[1];
            }
            if(ptr_idx == 1){
                ptr2 = ptr1[1];
            }
            if(ptr_idx == 2){
                ptr3 = ptr2[1];
            }
            if(ptr_idx == 3){
                ptr4 = ptr3[1];
            }
            if(ptr_idx == 4){
                ptr5 = ptr4[1];
            }
            if(ptr_idx == 5){
                ptr6 = ptr5[1];
            }
            if(ptr_idx == 6){
                ptr7 = ptr6[1];
            }
            if(ptr_idx == (7)){
                ptr8 = ptr7[1];
            }
            if(ptr_idx == (8)){
                ptr9 = ptr8[1];
            }
        } else {
            if(ptr_idx == 0){
                ptr1 = ptr[0];
            }
            if(ptr_idx == 1){
                ptr2 = ptr1[0];
            }
            if(ptr_idx == 2){
                ptr3 = ptr2[0];
            }
            if(ptr_idx == 3){
                ptr4 = ptr3[0];
            }
            if(ptr_idx == 4){
                ptr5 = ptr4[0];
            }
            if(ptr_idx == 5){
                ptr6 = ptr5[0];
            }
            if(ptr_idx == 6){
                ptr7 = ptr6[0];
            }
            if(ptr_idx == (7)){
                ptr8 = ptr7[0];
            }
            if(ptr_idx == (8)){
                ptr9 = ptr8[0];
            }
        }
        ptr_idx += 1;
        OBFS_IDX += 1;
        if(ptr_idx == (9)){
            out[write_idx/(8)] |= ((*ptr9) & ((1<<((8)-(write_idx%(8))))-1))<<(write_idx%(8));
            out[write_idx/(8) + 1] = (*ptr9) >> ((8)-(write_idx%(8)));
            ptr_idx = 0;
            write_idx += (9);
        }
    }
    for(size_t i = 0; i < (write_idx/(8)); i++){
        printf("%02x", (unsigned int)out[i]);
    }
    printf("\n");
}