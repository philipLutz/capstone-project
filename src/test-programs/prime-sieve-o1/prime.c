/*  Count prime numbers using Sieve of Eratosthenes
    Integer arithmetic, single dynamic memory allocation
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void sieve_of_e(uint8_t* nums, uint32_t length)
{
    for (uint32_t i = 2; i * i < length; i++) {
        if (!nums[i]) {
            for (uint32_t j = i * i; j <= length; j += i){
                nums[j]++;
            }
        }
    }
}


int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX - 1) {
            uint8_t* nums = (uint8_t*) calloc(num + 1, sizeof(uint8_t));
            sieve_of_e(nums, num + 1);

            uint32_t count = 0;
            for (uint32_t i = 2; i <= num; i++) {
                if (!nums[i]) {
                    count++;
                }
            }
            free(nums);
            printf("Total number of primes under %u: %u\n", num, count);
        } else {
            printf("Error: need positive argument less than %u\n", UINT32_MAX - 1);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
