#include "heap.h"
#include <sys/mman.h>



#ifndef HEAPHEAPHEAP_HEAPHEAP
#define HEAPHEAPHEAP_HEAPHEAP
struct HeapHeap {
    struct Heap heap;
    void *memory;
    void *top;
    size_t top_size;
};

void *halloc(size_t size);
void hfree(void *ptr);
void debug();
#endif