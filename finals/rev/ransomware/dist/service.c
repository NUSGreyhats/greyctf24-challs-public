#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


void setup() {
   setbuf(stdout, 0);
   setbuf(stdin, 0);
}

char *usernames[] = {"jro", "a", "b", "c", "d"};
char *passwords[] = {"Very secure pass", "a", "b", "c", "d"};
int len = 5;

int main(){
    setup();
    char username[0x10];
    char password[0x10];

    while(1) {
        printf("Enter username: ");
        gets(username);
        int found_id = -1;
        for(int i = 0; i < len; i++){
            if(!strcmp(usernames[i], username)){
                found_id = i;
                break;
            }
        }
        if(found_id == -1){
            printf("OOps! ");
            printf(username);
            printf(" is not a valid username!\n");
        } else {
            printf("Enter password: ");
            gets(password);
            if(strcmp(passwords[found_id],password)){
                printf("Wrong password!\n");
            } else {
                printf("Welcome ");
                printf(username);
                putchar('!');
                putchar('\n');
                return 0;
            }
        }
    }
}