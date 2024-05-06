/*  Multithread Linked List Search
    Find as many numbers in an unsorted linked list of random numbers
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>
#include <pthread.h>
#include <assert.h>

#define LIST_SIZE      50000000
#define NUM_MAX        200000000
#define NUM_THREADS    8


struct node {
    uint32_t value;
    struct node *next;
};

struct arg_t {
    uint32_t start;
    uint32_t stop;
    uint32_t count;
    struct node *list;
    struct node *head;
};

void* my_thread(void* arguments)
{
    struct arg_t *args = arguments;
    for (uint32_t i = args->start; i < args->stop; i++) {
        args->list = args->head;
        while (args->list->next != NULL) {
            if (args->list->value == i) {
                args->count += 1;
            }
            args->list = args->list->next;
        }
    }
    return NULL;
}

int main(int argc, char* argv[])
{
    pthread_t threads[NUM_THREADS];
    struct arg_t args[NUM_THREADS];
    uint64_t rc;

    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            srand(time(NULL));
            struct node *head = malloc(sizeof(struct node));
            struct node *list = head;
            for (uint32_t i = 0; i < LIST_SIZE; i++) {
                list->value = rand() % NUM_MAX;
                list->next = malloc(sizeof(struct node));
                list = list->next;
            }
            list->next = NULL;

            uint64_t sum_of_found = 0;
            uint32_t range = (num / NUM_THREADS) + 1;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                (args[i]).start = i * range;
                (args[i]).stop = ((i + 1) * range);
                (args[i].count) = 0;
                (args[i].list) = list;
                (args[i].head) = head;
            }
            (args[NUM_THREADS - 1]).stop = num;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_create(&threads[i], NULL, my_thread, (void *)&args[i]);
                assert(rc == 0);
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_join(threads[i], NULL);
                assert(rc == 0);
                sum_of_found += (args[i]).count;
            }

            list = head;
            struct node *previous;
            while (list != NULL) {
                previous = list;
                list = list->next;
                free(previous);
            }
            printf("Total found numbers: %" PRIu64 "\n", sum_of_found);
        } else {
            printf("Error: need positive argument less than %d\n", UINT32_MAX);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
