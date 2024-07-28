#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    FILE *fp;
    char flag[100];

    if (argc != 2 || strcmp(argv[1], "GIVEFLAGPLS") != 0) {
        printf("Usage: %s GIVEFLAGPLS\n", argv[0]);
        return 1;
    }

    fp = fopen("/flag", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    fgets(flag, 100, fp);
    printf("%s\n", flag);

    fclose(fp);
    return 0;
}