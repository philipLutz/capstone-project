/*  Matrix Multiply
    Heap allocated memory
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_SIZE            1000
#define MAX_ITERATIONS      10000000


int multiply_matrices(uint64_t** m1, uint64_t** m2, uint64_t** r, uint32_t size)
{
    for (uint32_t i = 0; i < size; i++) {
        for (uint32_t j = 0; j < size; j++) {
            r[i][j] = 0;
            for (uint32_t k = 0; k < size; k++) {
                r[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 3) {
        uint32_t num_size = (uint32_t) atoi(argv[1]);
        uint32_t num_iterations = (uint32_t) atoi(argv[2]);
        if (num_iterations > 0 && num_iterations < MAX_ITERATIONS && num_size > 0 && num_size < MAX_SIZE) {
            uint64_t** matrix_1 = malloc(num_size * sizeof(uint64_t*));
            uint64_t** matrix_2 = malloc(num_size * sizeof(uint64_t*));
            uint64_t** matrix_result = malloc(num_size * sizeof(uint64_t*));
            uint64_t k = 1;
            for (uint32_t i = 0; i < num_size; i++) {
                for (uint32_t j = 0; j < num_size; j++) {
                    matrix_1[i] = malloc(num_size * sizeof(uint64_t));
                    matrix_2[i] = malloc(num_size * sizeof(uint64_t));
                    matrix_result[i] = malloc(num_size * sizeof(uint64_t));
                    matrix_1[i][j] = k;
                    k++;
                    matrix_2[i][j] = k;
                    k++;
                }
            }
            uint32_t sum = 0;
            for (uint32_t i = 0; i < num_iterations; i++) {
                multiply_matrices(matrix_1, matrix_2, matrix_result, num_size);
                sum += ((matrix_result[num_size-1][num_size-1] - matrix_result[num_size-2][num_size-2])
                        / (num_size * num_size * num_size)) + 1;
                matrix_1[0][0] += sum;
                matrix_2[1][1] += sum + 1;
            }
            for (uint64_t i = 0; i < num_size; i++) {
                free(matrix_1[i]);
                free(matrix_2[i]);
                free(matrix_result[i]);
            }
            free(matrix_1);
            free(matrix_2);
            free(matrix_result);
            printf("%u\n", sum);
        } else {
            printf("Error: need positive argument less than %d\n", MAX_ITERATIONS);
            return 1;
        }
    } else {
        printf("Error: need one argument for number of iterations\n");
        return 1;
    }

    return 0;
}
