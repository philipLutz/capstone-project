/*  Linked List Search
    Find as many numbers in an unsorted linked list of random numbers
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>

#define LIST_SIZE      50000000
#define NUM_MAX        200000000


struct node {
    uint32_t value;
    struct node *next;
};

int main(int argc, char* argv[])
{
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
            for (uint32_t i = 0; i < num; i++) {
                list = head;
                while (list->next != NULL) {
                    if (list->value == i) {
                        sum_of_found++;
                    }
                    list = list->next;
                }
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
