/*  Find the Nth Number of the Fibonacci Sequence
    Memoized bottom-up implementation
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint64_t fib(uint8_t n) {
    // Upper limit of correctness is 94th, 2^64 size limit
    if (n == 1) {
        return 0;
    }
    if (n == 2) {
        return 1;
    }

    uint64_t current = 1;
    uint64_t previous = 0;
    uint64_t temp;
    uint8_t i = 2;
    while (i < n) {
        temp = current;
        current += previous;
        previous = temp;
        i++;
    }
    return current;
}

int main(int argc, char* argv[]) {
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            for (uint32_t i = 0; i < num; i++) {
                // ensure the argument is between [0, 94]
                fib(i % 95);
            }
        } else {
            printf("Error: need positive argument less than %u\n", UINT32_MAX);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
