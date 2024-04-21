#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>



void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}


char output[0x20];
char command[0x20];


void goodbye(){
    puts("Adiós!");
    system(command);
}



void print_time(){
    time_t now;
    struct tm *time_struct;
    char input[0x20];
    char buf[0x30];

    time(&now);
    time_struct = localtime(&now);

    printf("The time now is %d.\nEnter format specifier: ", now);
    fgets(input, 0x20, stdin);

    for(int i = 0; i < strlen(input)-1; i++){
        if(i % 2 == 0 && input[i] != '%'){
            puts("Only format specifiers allowed!");
            exit(0);
        }
    }

    strftime(buf, 0x30, input, time_struct);
    // remove newline at the end
    buf[strlen(buf)-1] = '\0';

    memcpy(output, buf, strlen(buf));
    printf("Formatted: %s\n", output);
}


void set_locale(){
    char input[0x20];
    printf("Enter new locale: ");
    fgets(input, 0x20, stdin);
    char *result = setlocale(LC_TIME, input);
    if(result == NULL){
        puts("Failed to set locale :(");
        puts("Run locale -a for a list of valid locales.");
    }else{
        puts("Locale changed successfully!");
    }
}

int main(){
    int choice = 0;

    setup();

    strcpy(command, "ls");

    while (1){
        puts("Welcome to international time converter!");
        puts("Menu:");
        puts("1. Print time");
        puts("2. Change language");
        puts("3. Exit");
        printf("> ");

        scanf("%d", &choice);
        getchar();

        if(choice == 1){
            print_time();
        }else if(choice == 2){
            set_locale();
        }else{
            goodbye();
        }
        puts("");
    }
}