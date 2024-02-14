#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>

#define ITERATIONS 1000

int cp(const char* to, const char* from) {
    int fd_to, fd_from;
    char buffer[4096];
    ssize_t nread;
    int saved_errno;

    fd_from = open(from, O_RDONLY);
    if (fd_from < 0) {
        return -1;
    }

    fd_to = open(to, O_WRONLY | O_CREAT | O_EXCL | O_DSYNC, 0700);
    if (fd_to < 0) {
        goto out_error;
    }

    while (nread = read(fd_from, buffer, sizeof buffer), nread > 0) {
        char* out_ptr = buffer;
        ssize_t nwritten;

        do {
            nwritten = write(fd_to, out_ptr, nread);

            if (nwritten >= 0) {
                nread -= nwritten;
            }
            else if (errno != EINTR) {
                goto out_error;
            }
        } while (nread > 0);
    }

    if (nread == 0) {
        if (close(fd_to) < 0) {
            fd_to = -1;
            goto out_error;
        }
        close(fd_from);

        return 0;
    }

    out_error:
        saved_errno = errno;

        close(fd_from);
        if (fd_to >= 0) {
            close(fd_to);
        }

        errno = saved_errno;
        return -1;
}

int main(void) {
    for (int i = 0; i < ITERATIONS; i++) {
        // "matrix.txt" must be in the directory that this program is called from
        if (cp("test.txt", "matrix.txt") == 0) {
            if (remove("test.txt") < 0) {
                printf("Failed to remove test file\n");
            }
        }
    }

    return 0;
}
