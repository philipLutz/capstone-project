/*  Matrix Multiply
    Stack allocated memory
    Fixed Size Matrices
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MATRIX_SIZE         100
#define MAX_ITERATIONS      10000000


int multiply_matrices(uint64_t m1[MATRIX_SIZE][MATRIX_SIZE], uint64_t m2[MATRIX_SIZE][MATRIX_SIZE], uint64_t r[MATRIX_SIZE][MATRIX_SIZE])
{
    for (uint64_t i = 0; i < MATRIX_SIZE; i++) {
        for (uint64_t j = 0; j < MATRIX_SIZE; j++) {
            r[i][j] = 0;
            for (uint64_t k = 0; k < MATRIX_SIZE; k++) {
                r[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < MAX_ITERATIONS) {
            uint64_t matrix_1[MATRIX_SIZE][MATRIX_SIZE];
            uint64_t matrix_2[MATRIX_SIZE][MATRIX_SIZE];
            uint64_t matrix_result[MATRIX_SIZE][MATRIX_SIZE];
            uint64_t k = 1;
            for (uint64_t i = 0; i < MATRIX_SIZE; i++) {
                for (uint64_t j = 0; j < MATRIX_SIZE; j++) {
                    matrix_1[i][j] = k;
                    k++;
                    matrix_2[i][j] = k;
                    k++;
                }
            }
            uint32_t sum = 0;
            for (uint32_t i = 0; i < num; i++) {
                multiply_matrices(matrix_1, matrix_2, matrix_result);
                sum += ((matrix_result[MATRIX_SIZE-1][MATRIX_SIZE-1] - matrix_result[MATRIX_SIZE-2][MATRIX_SIZE-2])
                        / (MATRIX_SIZE * MATRIX_SIZE * MATRIX_SIZE));
            }
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
