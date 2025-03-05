#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Define the maximum number of buckets in the hash table
#define BUCKETS (101)

// Define a structure for a linked list node
typedef struct node {
    int key;
    struct node *next;
} node_t;

// Define a structure for a linked list
typedef struct list {
    node_t *head;
    pthread_mutex_t lock;
} list_t;

// Define a structure for the concurrent hash table
typedef struct __hash_t {
    list_t lists[BUCKETS];
} hash_t;

// Initialize the linked list
void List_Init(list_t *L) {
    L->head = NULL;
    pthread_mutex_init(&L->lock, NULL);
}

// Insert a new node with the given key at the beginning of the list
int List_Insert(list_t *L, int key) {
    // Allocate memory for a new node
    node_t *new = malloc(sizeof(node_t));
    if (new == NULL) {
        perror("malloc");
        return -1; // Return -1 on failure
    }
    new->key = key;

    // Lock the critical section
    pthread_mutex_lock(&L->lock);

    // Update the pointers to insert the new node at the beginning
    new->next = L->head;
    L->head = new;

    // Unlock the critical section
    pthread_mutex_unlock(&L->lock);

    return 0; // Return 0 on success
}

// Lookup a key in the linked list and return 0 if found, -1 if not found
int List_Lookup(list_t *L, int key) {
    int rv = -1;

    // Lock the critical section
    pthread_mutex_lock(&L->lock);

    // Traverse the linked list to find the key
    node_t *curr = L->head;
    while (curr) {
        if (curr->key == key) {
            rv = 0; // Key found
            break;
        }
        curr = curr->next;
    }

    // Unlock the critical section
    pthread_mutex_unlock(&L->lock);

    return rv; // Return 0 for success and -1 for failure
}

// Initialize the concurrent hash table
void Hash_Init(hash_t *H) {
    int i;
    for (i = 0; i < BUCKETS; i++)
        List_Init(&H->lists[i]);
}

// Insert a key into the hash table
int Hash_Insert(hash_t *H, int key) {
    return List_Insert(&H->lists[key % BUCKETS], key);
}

// Lookup a key in the hash table
int Hash_Lookup(hash_t *H, int key) {
    return List_Lookup(&H->lists[key % BUCKETS], key);
}
