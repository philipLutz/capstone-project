/*  Collatz Conjecture
    Find the number that takes the most steps to approach 1 when applying n / 2 and 3n + 1
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

uint64_t collatz(uint32_t num)
{
    uint64_t i = 0;
    while (num > 1) {
        if (num % 2 == 0) {
            num = num / 2;
        } else {
            num = (3 * num) + 1;
        }
        i++;
    }
    return i;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint64_t max_steps = 0;
            uint32_t max_num = 0;
            for (uint32_t i = 0; i <= num; i++) {
                uint64_t steps = collatz(i);
                if (steps > max_steps) {
                    max_steps = steps;
                    max_num = i;
                }
            }
            printf("Max Steps: %" PRIu64 ", Number: %u\n", max_steps, max_num);
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
