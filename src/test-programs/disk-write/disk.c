/*  Write and Remove File
    Program has to wait for user space buffer to flush
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int write_and_remove_file(uint32_t iterations)
{
    char* file_name= "disk_test.txt";

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

    for (uint32_t i = 0; i < iterations; i++) {
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

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            write_and_remove_file(num);
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
