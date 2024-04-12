/*  Get an array of random unsigned integers
    Dynamically allocated memory
    Read from /dev/urandom
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>


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

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            uint64_t* array = malloc(num * sizeof(uint64_t));
            uint64_t i = 0;
            while (i < num) {
                array[i] = get_random_number();
                i++;
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
