#include "heapheap.h"
#include <string.h>

void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

size_t read_number() {
    size_t result = 0;

    scanf("%zu", &result);
    getchar();

    if (result > 0)
    {
        return result;
    }

    exit(-1);
}


void read_node(struct Node *node) {
    printf("Enter length of str: ");
    size_t len = read_number();

    char *out = halloc(len);

    printf("Enter string: ");

    fgets(out, len, stdin);
    if(out[strlen(out)-1] == '\n')
        out[strlen(out)-1] = '\0';


    printf("Enter value: ");
    size_t value = read_number();

    node->value = value;
    node->data = out;
}


struct Heap heap = {
    .max = NULL,
    .num_nodes = 0,
};

void backdoor() {
    system("/bin/sh");
}


int main() {
    setup();

    int opt;

    while(true) {
        puts("Menu:");
        puts("1. Add node");
        puts("2. Edit root");
        puts("3. Delete root");
        puts("4. Exit");
        printf("Your choice: ");

        scanf("%d", &opt);
        getchar();

        if(opt == 1) {
            struct Node *node = halloc(NODE_SIZE);
            read_node(node);
            insert(&heap, node);
        } else if(opt == 2) {
            struct Node *max = heap.max;
            del_node(&heap, max);
            hfree(max->data);
            max->data = NULL;
            read_node(max);
            insert(&heap, max);
        } else if(opt == 3) {
            struct Node *max = heap.max;
            printf("The largest element is '%s' with a value of %d", max->data, max->value);
            del_node(&heap, max);
            hfree(max->data);
            max->data = NULL;
            hfree(max);
        } else {
            exit(0);
        }
        puts("");
        puts("The heap:");
        print2D(heap.max);
        puts("");
    }
}