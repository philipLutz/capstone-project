/*  Find the Nth Number of the Fibonacci Sequence
    Naive recursive top-down implementation
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define NUM_LIMIT   50

uint64_t fib(uint8_t n) {
    if (n == 1) {
        return 0;
    }
    if (n == 2) {
        return 1;
    }
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char* argv[]) {
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < NUM_LIMIT) {
            fib(num);
        } else {
            printf("Error: need positive argument less than %d\n", NUM_LIMIT);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
