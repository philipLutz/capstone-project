
#include <stdio.h>

#define ITERATIONS 100000

int main(void) {
    char* file_name= "test.txt";

    for (int i = 0; i < ITERATIONS; i++) {
        // Open file for writing
        FILE *f = fopen(file_name, "a");
        if (f == NULL) {
            printf("Error opening file!\n");
            return 1;
        }
        // Write some stuff
        if (i % 10 == 0) {
            fprintf(f, "\n");
        }
        fprintf(f, "%d ", i);
        // Close the file
        fclose(f);
    }

    if (remove(file_name) == 0) {
        return 0;
    }
    printf("Failed to delete test file");
    return 1;
}
