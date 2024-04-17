/*  String Resizing
    Dynamically allocated memory
    Small string
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


const char* keeps_changing_size = "why does this keep changing size! ";
const uint8_t keeps_changing_size_size = 36;

int string_realloc(uint32_t iterations)
{
    char* string = (char *) malloc(keeps_changing_size_size * sizeof(char));
    strncpy(string, keeps_changing_size, keeps_changing_size_size);

    uint32_t i = 0;
    uint32_t size_multiplier = 2;
    while (i < iterations) {
        if (size_multiplier == 500) {
            size_multiplier = 1;
        }
        string = (char *) realloc(string, keeps_changing_size_size * size_multiplier * sizeof(char));
        uint32_t k = 0;
        for (uint32_t j = 0; j < keeps_changing_size_size * size_multiplier; j++) {
            if (k == keeps_changing_size_size - 1) {
                k = 0;
            }
            string[j] = keeps_changing_size[k];
            k++;
            if (j == (keeps_changing_size_size * size_multiplier) - 2) {
                string[j] = '\0';
            }
        }
        size_multiplier++;
        i++;
    }

    free(string);

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            string_realloc(num);
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
