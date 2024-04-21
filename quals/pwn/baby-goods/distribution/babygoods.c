#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char username[0x20];

int menu(char name[0x20]);

int sub_15210123() {
    execve("/bin/sh", 0, 0);
}

int buildpram() {
    char buf[0x10];
    char size[4];
    int num;

    printf("\nChoose the size of the pram (1-5): ");
    fgets(size,4,stdin);
    size[strcspn(size, "\r\n")] = '\0';
    num = atoi(size);
    if (1 > num || 5 < num) {
        printf("\nInvalid size!\n");
        return 0;
    }

    printf("\nYour pram has been created! Give it a name: ");
    //buffer overflow! user can pop shell directly from here
    gets(buf);
    printf("\nNew pram %s of size %s has been created!\n", buf, size);
    return 0;
}

int exitshop() {
    puts("\nThank you for visiting babygoods!\n");
    exit(0);
}

int menu(char name[0x20]) {
    char input[4];
    do {
        printf("\nHello %s!\n", name);
        printf("Welcome to babygoods, where we provide the best custom baby goods!\nWhat would you like to do today?\n");
        printf("1: Build new pram\n");
        printf("2: Exit\n");
        printf("Input: ");
        fgets(input, 4, stdin);
        input[strcspn(input, "\r\n")] = '\0';
        switch (atoi(input))
        {
        case 1:
            buildpram();
            break;
        default:
            printf("\nInvalid input!\n==========\n");
            menu(name);
        }
    } while (atoi(input) != 2);
    exitshop();
}

int main() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);

    printf("Enter your name: ");
    fgets(username,0x20,stdin);
    username[strcspn(username, "\r\n")] = '\0';
    menu(username);
    return 0;
}
