
#include <stdio.h>

#define ITERATIONS 100000


int main(void) {
    char* file_name= "test.txt";

    FILE* f = fopen(file_name, "w+");
    if (f == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    int c = 0;
    fpos_t pos;
    fgetpos(f, &pos);
    fputc(c, f);
    fflush(f);

    for (int i = 0; i < ITERATIONS; i++) {
        fsetpos(f, &pos);
        c = fgetc(f);
        c = (c + 1) % 128;
        fgetpos(f, &pos);
        fputc(c, f);
        fflush(f);
    }
    fclose(f);

    if (remove(file_name) == 0) {
        return 0;
    }
    printf("Failed to delete test file");
    return 1;
}
