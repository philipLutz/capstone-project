/*  Multithread count prime numbers
    Integer arithmetic
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#include <assert.h>

#define NUM_THREADS     8

int is_prime(uint32_t num)
{
    if (num < 4) {
        if (num <= 1) {
            return 0;
        }
        return 1;
    }

    for (uint32_t i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return 0;
        }
    }
    return 1;
}

struct arg_t {
    uint32_t start;
    uint32_t stop;
    uint32_t count;
};

void* my_thread(void* arguments)
{
    struct arg_t *args = arguments;
    for (uint32_t i = args->start; i < args->stop; i++) {
        if (is_prime(i)) {
            args->count += 1;
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
            uint32_t count = 0;
            uint32_t range = (num / NUM_THREADS) + 1;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                (args[i]).start = i * range;
                (args[i]).stop = ((i + 1) * range);
                (args[i].count) = 0;
            }
            (args[NUM_THREADS - 1]).stop = num;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_create(&threads[i], NULL, my_thread, (void *)&args[i]);
                assert(rc == 0);
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_join(threads[i], NULL);
                assert(rc == 0);
                count += (args[i]).count;
            }
            printf("Total number of primes under %d: %d\n", num, count);
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
