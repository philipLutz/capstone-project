
#include <stdio.h>

#define NTH_NUM 40

long unsigned fib(long unsigned n) {
    if (n == 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return fib(n - 1) + fib(n - 2);
}

int main(void) {
    printf("%lu\n", fib(NTH_NUM));

    return 0;
}


