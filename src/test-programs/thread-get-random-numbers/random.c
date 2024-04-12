/*  Get an array of random unsigned integers
    Multithread
    Dynamically allocated memory
    Read from /dev/urandom
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <assert.h>

#define NUM_THREADS     8


uint64_t get_random_number(void)
{
    uint64_t num = 0;
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd >= 0) {
        read(fd, (uint64_t*) &num, sizeof(num));
        close(fd);
    }
    return num;
}

struct arg_t {
    uint32_t start;
    uint32_t stop;
    uint64_t* array;
};

void* my_thread(void* arguments)
{
    struct arg_t *args = arguments;
    for (uint32_t i = args->start; i < args->stop; i++) {
        (args->array)[i] = get_random_number();
    }
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
            uint64_t* array = malloc(num * sizeof(uint64_t));
            uint32_t range = (num / NUM_THREADS) + 1;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                (args[i]).start = i * range;
                (args[i]).stop = ((i + 1) * range);
                (args[i]).array = array;
            }
            (args[NUM_THREADS - 1]).stop = num;
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_create(&threads[i], NULL, my_thread, (void *)&args[i]);
                assert(rc == 0);
            }
            for (uint8_t i = 0; i < NUM_THREADS; i++) {
                rc = pthread_join(threads[i], NULL);
                assert(rc == 0);
            }
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
