#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#ifndef HEAPHEAPHEAP_HEAP
#define HEAPHEAPHEAP_HEAP

#define NODE_SIZE 40

struct Node {
    size_t value;
    struct Node *left;
    struct Node *right;
    struct Node *parent;
    void *data;
};

struct Heap {
    struct Node *max;
    unsigned char num_nodes;
};

void assert(bool x, char *msg);
void print2DUtil(struct Node* root, int space);
void print2D(struct Node* root);
void update_children_parent(struct Node *node);
void swap(struct Heap *heap, struct Node *parent, struct Node *child);
void insert(struct Heap *heap, struct Node *node);
void del_node(struct Heap *heap, struct Node *node);
struct Node *make(size_t value);
#endif