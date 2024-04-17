/*  Sort an array of unsigned integers
    Dynamically allocated memory
    Random input
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>


int bubble_sort(uint32_t* array, uint32_t size)
{
    uint8_t swapped = 0;
    for (uint32_t i = 0; i < size - 1; i++) {
        swapped = 0;
        for (uint32_t j = 0; j < size - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                swapped = 1;
                uint32_t temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
        if (swapped == 0) {
            break;
        }
    }
    return 0;
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
            bubble_sort(array, num);
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
