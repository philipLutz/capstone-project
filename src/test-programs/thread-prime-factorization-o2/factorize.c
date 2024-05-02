/*  Multithread Prime Factorization
    Sum of primes factors of all numbers up to and including argument
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <pthread.h>
#include <assert.h>

#define NUM_THREADS     5

uint64_t sum_prime_factors(uint64_t n)
{
    uint64_t sum = 0;
    while (n % 2 == 0) {
        sum += 2;
        n = n / 2;
    }
    for (uint64_t i = 3; (i * i) <= n; i += 2) {
        while (n % i == 0) {
            sum += i;
            n = n / i;
        }
    }
    if (n > 2) {
        sum += n;
    }
    return sum;
}

struct arg_t {
    uint64_t start;
    uint64_t stop;
    uint64_t sum;
};

void* my_thread(void* arguments)
{
    struct arg_t *args = arguments;
    for (uint64_t i = args->start; i < args->stop; i++) {
        args->sum += sum_prime_factors(i);
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
            uint64_t sum_of_factors = 0;
            uint64_t range = (num / NUM_THREADS) + 1;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                (args[i]).start = i * range;
                if (i == 0) {
                    (args[i]).start = 4;
                }
                (args[i]).stop = ((i + 1) * range);
                (args[i].sum) = 0;
            }
            (args[NUM_THREADS - 1]).stop = num;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_create(&threads[i], NULL, my_thread, (void *)&args[i]);
                assert(rc == 0);
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_join(threads[i], NULL);
                assert(rc == 0);
                sum_of_factors += (args[i]).sum;
            }
            printf("Sum of prime factors: %" PRIu64 "\n", sum_of_factors);
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
