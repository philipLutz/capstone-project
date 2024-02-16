/*  Add integers
    Pathological example of simple arithmetic 
    There should be an efficient use of CPU cache,
    and instructions per cycle should be close to superscalar limits of a single CPU core
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int add(uint32_t iterations)
{
    uint32_t a = 0;
    uint32_t b = 0;
    uint32_t c = 0;
    uint32_t d = 0;
    uint32_t e = 0;
    uint64_t sum = 0;

    for (uint32_t i = 0; i < iterations; i++) {
        while (sum < UINT32_MAX) {
            sum += a + b + c + d + e;
            a++;
            b++;
            c++;
            d++;
            e++;
        }
        // set all values back to zero before starting next iteration
        a = 0;
        b = 0;
        c = 0;
        d = 0;
        e = 0;
        sum = 0;
    }

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            add(num);
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
