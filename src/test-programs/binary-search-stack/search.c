/*  Binary Search
    Find random number in a sorted stack-allocated array
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>

#define ARRAY_SIZE      1000000


int32_t binary_search(uint32_t array[], uint32_t left, uint32_t right, uint32_t num)
{
    if (left < right) {
        uint32_t middle = (left + (right - 1)) / 2;
        if (array[middle] == num) {
            return middle;
        }
        if (array[middle] > num) {
            return binary_search(array, left, middle - 1, num);
        }
        return binary_search(array, middle + 1, right, num);
    }
    return -1;
}

int compare_function(const void * a, const void * b)
{
    return ( *(uint32_t*)a - *(uint32_t*)b );
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint32_t array[ARRAY_SIZE];
            srand(time(NULL));
            for (uint32_t i = 0; i < ARRAY_SIZE; i++) {
                array[i] = rand() % ARRAY_SIZE;
            }
            qsort(array, ARRAY_SIZE, sizeof(uint32_t), compare_function);

            uint64_t sum_of_indexes = 0;
            for (uint32_t i = 0; i < num; i++) {
                uint32_t random_number = rand() % ARRAY_SIZE;
                if (binary_search(array, 0, (ARRAY_SIZE - 1), random_number) > 0) {
                    sum_of_indexes++;
                }
            }
            printf("Total found numbers: %" PRIu64 "\n", sum_of_indexes);
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
