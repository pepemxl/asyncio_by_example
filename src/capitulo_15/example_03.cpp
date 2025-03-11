#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <assert.h>

typedef struct __node_t {
    int value;
    struct __node_t *next;
} node_t;

typedef struct __queue_t {
    node_t *head;
    node_t *tail;
    pthread_mutex_t head_lock, tail_lock;
} queue_t;

void Queue_Init(queue_t *q) {
    node_t *tmp = (node_t *)malloc(sizeof(node_t)); // Cast to node_t*
    tmp->next = NULL;
    q->head = q->tail = tmp;
    pthread_mutex_init(&q->head_lock, NULL);
    pthread_mutex_init(&q->tail_lock, NULL);
}

void Queue_Enqueue(queue_t *q, int value) {
    node_t *tmp = (node_t *)malloc(sizeof(node_t)); // Cast to node_t*
    assert(tmp != NULL);
    tmp->value = value;
    tmp->next = NULL;

    pthread_mutex_lock(&q->tail_lock);
    q->tail->next = tmp;
    q->tail = tmp;
    pthread_mutex_unlock(&q->tail_lock);
}


int Queue_Dequeue(queue_t *q, int *value) {
    pthread_mutex_lock(&q->head_lock);
    node_t *tmp = q->head;
    node_t *new_head = tmp->next;
    if (new_head == NULL) {
        pthread_mutex_unlock(&q->head_lock);
        return -1; // queue was empty
    }
    *value = new_head->value;
    q->head = new_head;
    pthread_mutex_unlock(&q->head_lock);
    free(tmp);
    return 0;
}

void* EnqueueThread(void *arg) {
    queue_t *q = (queue_t*)arg;
    for (int i = 0; i < 5; ++i) {
        Queue_Enqueue(q, i);
        printf("Enqueued %d\n", i);
    }
    return NULL;
}

void* DequeueThread(void *arg) {
    queue_t *q = (queue_t*)arg;
    int value;
    for (int i = 0; i < 5; ++i) {
        if (Queue_Dequeue(q, &value) != -1) {
            printf("Dequeued %d\n", value);
        } else {
            printf("Queue is empty\n");
        }
    }
    return NULL;
}

int main() {
    queue_t queue;
    Queue_Init(&queue);

    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, EnqueueThread, &queue);
    pthread_create(&thread2, NULL, DequeueThread, &queue);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    return 0;
}
