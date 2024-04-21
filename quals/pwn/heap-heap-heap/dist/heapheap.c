#include "heapheap.h"

#define MEM_SIZE 0x1000

char mem[MEM_SIZE];

struct HeapHeap heap_heap = {
    .heap = {
        .max = NULL,
        .num_nodes = 0,
    },
    .memory = mem,
    .top = mem,
    .top_size = MEM_SIZE,
};

void *halloc(size_t size) {
    assert(heap_heap.top != NULL, "heap not initialized yet");

    if(heap_heap.heap.num_nodes == 0 || heap_heap.heap.max->value < size) {
        // New chunk needed
        size_t memory_needed = NODE_SIZE + size;
        if(memory_needed > heap_heap.top_size) {
            puts("Memory size exceeded");
            exit(-1);
        }

        struct Node *node = heap_heap.top;
        node->parent = NULL;
        node->left = NULL;
        node->right = NULL;
        node->value = size;
        node->data = heap_heap.top + NODE_SIZE;

        heap_heap.top += memory_needed;
        heap_heap.top_size -= memory_needed;

        return node->data;
    }

    // Split old node into new node to service allocation and remainder
    struct Node *node = heap_heap.heap.max;
    size_t old_size = node->value;
    del_node(&heap_heap.heap, node);
    node->value = size;

    if(old_size == size) {
        return node->data;
    }
    
    struct Node *new_node = node->data + size;
    new_node->data = (void*)new_node + NODE_SIZE;
    new_node->value = old_size - NODE_SIZE - size;
    insert(&heap_heap.heap, new_node);

    return node->data;
}

void hfree(void *ptr) {
    struct Node *node = ptr - NODE_SIZE;
    insert(&heap_heap.heap, node);
}

void debug() {
    puts("halloc heap:");
    print2D(heap_heap.heap.max);
}