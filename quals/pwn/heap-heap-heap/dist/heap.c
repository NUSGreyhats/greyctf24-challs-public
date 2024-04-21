#include "heap.h"


void assert(bool x, char *msg){
    if(!x){
        printf("Assertion failed: %s\n", msg);
        exit(-1);
    }
}

// From https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
void print2DUtil(struct Node* root, int space)
{
    // Base case
    if (root == NULL)
        return;
 
    // Increase distance between levels
    space += 10;
 
    // Process right child first
    if(root->right != NULL){
        assert(root->right != root, "right loop detected");
    }
    print2DUtil(root->right, space);
 
    // Print current node after space
    // count
    printf("\n");
    for (int i = 10; i < space; i++)
        printf(" ");
    printf("%zu\n", root->value);
 
    // Process left child
    if(root->left != NULL) {
        assert(root->left != root, "left loop detected");
    }
    print2DUtil(root->left, space);
    
}
 
// Wrapper over print2DUtil()
void print2D(struct Node* root)
{
    // Pass initial space count as 0
    print2DUtil(root, 0);
}

void update_children_parent(struct Node *node) {
    if(node->left != NULL) {
        node->left->parent = node;
    }
    if(node->right != NULL) {
        node->right->parent = node;
    }
}

// Maybe pointer based heap was a bad idea :thinking:
void swap(struct Heap *heap, struct Node *parent, struct Node *child) {
    assert(child->parent == parent, "Child is not related to parent");
    assert(parent != child, "Loop detected");

    struct Node *grandparent = parent->parent;
    struct Node *tmp;

    if(grandparent != NULL) {
        if(grandparent->left == parent) {
            grandparent->left = child;
        } else {
            grandparent->right = child;
        }
    } else {
        heap->max = child;
    }

    child->parent = grandparent;
    parent->parent = child;

    // This bit has too many pointers :(
    if(parent->left == child) {
        tmp = parent->right;
        parent->left = child->left;
        parent->right = child->right;
        child->right = tmp;
        child->left = parent;
    }else if(parent->right == child) {
        tmp = parent->left;
        parent->left = child->left;
        parent->right = child->right;
        child->left = tmp;
        child->right = parent;
    }else {
        puts("Child is not related to parent");
        exit(-1);
    }

    update_children_parent(child);
    update_children_parent(parent);
}

void insert(struct Heap *heap, struct Node *node) {
    if(heap->num_nodes >= 255) {
        puts("Too many nodes!");
        exit(-1);
    }

    node->left = NULL;
    node->right = NULL;
    node->parent = NULL;

    heap->num_nodes += 1;

    if(heap->max == NULL) {
        heap->max = node;
        return;
    }

    struct Node *cur = heap->max;
    struct Node *next = NULL;
    unsigned char num_nodes = heap->num_nodes;

    // https://stackoverflow.com/a/28397137/11168593
    bool has_one = false;
    for(int i = 7; i >= 0; i -= 1) {
        bool bit = num_nodes & (1 << i);
        if(!has_one) {
            has_one = bit;
            continue;
        }
        if(bit) {
            next = cur->right;
        } else {
            next = cur->left;
        }
        if(next == NULL){
            break;
        }
        cur = next;
    }
    if(cur->left == NULL){
        cur->left = node;
        node->parent = cur;
    } else {
        cur->right = node;
        node->parent = cur;
    }

    while(node->parent != NULL) {
        if(node->value > node->parent->value){
            swap(heap, node->parent, node);
        } else {
            break;
        }
    }
}

// Pretty standard heap deletion
void del_node(struct Heap *heap, struct Node *node) {
    assert(node != NULL, "cannot delete null node");
    while(node->left != NULL || node->right != NULL) {
        if(node->left != NULL && node->right != NULL) {
            if(node->left->value > node->right->value) {
                swap(heap, node, node->left);
            } else {
                swap(heap, node, node->right);
            }
        } else if(node->left != NULL) {
            swap(heap, node, node->left);
        } else {
            swap(heap, node, node->right);
        }
    }
    assert(node->left == NULL, "node left is not null");
    assert(node->right == NULL, "node right is not null");
    struct Node *parent = node->parent;
    if(parent == NULL) {
        heap->max = NULL;
    } else {
        if(parent->left == node) {
            parent->left = NULL;
        } else {
            parent->right = NULL;
        }
    }
    node->parent = NULL;
    heap->num_nodes -= 1;
}


struct Node *make(size_t value) {
    struct Node *node = calloc(1, sizeof(struct Node));
    node->value = value;
    return node;
}