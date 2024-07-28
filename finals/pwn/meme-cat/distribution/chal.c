#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}


int read_number() {
    int result = -1;

    scanf("%d", &result);
    getchar();

    if (result > -1)
    {
        return result;
    }

    exit(-1);
}

char *read_meme(int *len) {
    printf("Enter length of meme: ");
    *len = read_number();

    char *out = malloc((size_t)*len + 1);

    if (out == NULL)
    {
        exit(-1);
    }

    printf("Enter meme: ");

    fgets(out, *len + 1, stdin);

    return out;
}

void meme_cat() {

    int x, y;
    char *a = read_meme(&x);
    char *b = read_meme(&y);
    char *c = malloc((size_t)(x + y));

    for(int i = 0; i < x; i++) {
        *(c++) = *(a++);
    }
    for(int i = 0; i < y; i++) {
        *(c++) = *(b++);
    }

    puts(c);

    free(c);
    free(b);
    free(a);
}

int main() {
    setup();
    while (true)
    {
        meme_cat();
    }
}
