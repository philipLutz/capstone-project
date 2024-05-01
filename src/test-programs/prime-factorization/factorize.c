/*  Prime Factorization
    Sum of primes factors of all numbers up to and including argument
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

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

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint64_t sum_of_factors = 0;
            for (uint64_t i = 4; i <= num; i++) {
                sum_of_factors += sum_prime_factors(i);
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
