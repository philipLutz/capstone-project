/*  Multithread Write and Remove File
    Program has to wait for user space buffer to flush
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#include <assert.h>

#define NUM_THREADS     8

int write_and_remove_file(uint32_t iterations, uint8_t id)
{
    char file_name[16];
    snprintf(file_name, 16, "disk_test%d.txt", id);

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

struct arg_t {
    uint32_t iterations;
    uint8_t id;
};

void* my_thread(void* arguments)
{
    struct arg_t *args = arguments;
    write_and_remove_file(args->iterations, args->id);
    return NULL;
}

int main(int argc, char* argv[])
{
    pthread_t threads[NUM_THREADS];
    struct arg_t args[NUM_THREADS];
    uint64_t rc;

    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                (args[i]).iterations = num;
                (args[i]).id = i;
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_create(&threads[i], NULL, my_thread, (void *)&args[i]);
                assert(rc == 0);
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_join(threads[i], NULL);
                assert(rc == 0);
            }
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
