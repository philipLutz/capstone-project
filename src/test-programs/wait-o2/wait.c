/*  Wait for a time
    Do nothing while waiting for a time, sleep
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>


int wait_seconds(uint32_t seconds)
{
    time_t start = time(NULL);
    time_t end = time(NULL);
    while (difftime(end, start) <= seconds) {
        end = time(NULL);
    }
    return 0;
}

int main(int argc, char* argv[])
{
    if (argc == 2) {
        uint32_t num = (uint32_t) atoi(argv[1]);
        if (num > 0 && num < UINT32_MAX) {
            wait_seconds(num);
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
