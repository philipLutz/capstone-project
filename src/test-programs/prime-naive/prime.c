/*  Count prime numbers
    Integer arithmetic
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

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

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint32_t count = 0;
            for (uint32_t i = 1; i < num; i++) {
                if (is_prime(i)) {
                    count++;
                }
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
