/**
 * Unsigned integer add in an infinite loop
 * Used for measuring off-CPU time with cpudist-bpfcc
*/

#include <limits.h>

int main(void) {
    while (1) {
        unsigned a = 0;
        unsigned b = 0;
        unsigned c = 0;
        unsigned d = 0;
        unsigned e = 0;
        unsigned f = 0;
        unsigned g = 0;
        while (a + b + c + d + e + f + g < INT_MAX) {
            a++;
            b++;
            c++;
            d++;
            e++;
            f++;
            g++;
        }
    }

    return 0;
}
