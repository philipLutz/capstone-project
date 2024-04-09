/*  Sort an array of unsigned integers
    Dynamically allocated memory
    Random input
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>


int compare_function(const void * a, const void * b)
{
    return ( *(uint32_t*)a - *(uint32_t*)b );
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint32_t* array = malloc(num * sizeof(uint32_t));
            srand(time(NULL));
            uint32_t i = 0;
            while(i < num) {
                array[i] = (uint32_t) (rand() % num);
                i++;
            }
            qsort(array, num, sizeof(uint32_t), compare_function);
            free(array);
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
