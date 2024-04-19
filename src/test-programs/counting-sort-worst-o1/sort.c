/*  Sort an array of unsigned integers
    Dynamically allocated memory
    Worst case input
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_SIZE      ((UINT32_MAX - 1) / 5)


uint32_t get_max_value(uint32_t* array, uint32_t size)
{
    uint32_t max_num = 0;
    for (uint32_t i = 0; i < size; i++) {
        if (array[i] > max_num) {
            max_num = array[i];
        }
    }
    return max_num;
}

int counting_sort(uint32_t* array, uint32_t size)
{
    uint32_t max_num = get_max_value(array, size);

    uint32_t* counts = calloc(max_num + 1, sizeof(uint32_t));
    if (counts == NULL) {
        printf("calloc() failed\n");
        return 1;
    }

    for (uint32_t i = 0; i < size; i++) {
        (counts[array[i]])++;
    }
    for (uint32_t i = 1; i <= max_num; i++) {
        counts[i] += counts[i - 1];
    }

    uint32_t* temp_array = malloc(size * sizeof(uint32_t));
    if (temp_array == NULL) {
        printf("malloc() failed\n");
        return 1;
    }
    for (uint32_t i = size - 1; i >= 0; i--) {
        (counts[array[i]])--;
        temp_array[counts[array[i]]] = array[i];
        if (i == 0) {
            break;
        }
    }
    
    for (uint32_t i = 0; i < size; i++) {
        array[i] = temp_array[i];
    }

    free(temp_array);
    free(counts);

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < MAX_SIZE) {
            uint32_t* array = malloc(num * sizeof(uint32_t));
            uint32_t i = 0;
            uint32_t j = MAX_SIZE;
            while(i < num) {
                if (j == 0) {
                    j = MAX_SIZE;
                }
                array[i] = j;
                i++;
                j--;
            }
            counting_sort(array, num);
            free(array);
        } else {
            printf("Error: need positive argument less than %d\n", MAX_SIZE);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
