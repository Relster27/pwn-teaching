#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// gcc chall.c -o chall -fno-stack-protector -no-pie -z now

void gadget(void)
{
        asm("pop %rsp; ret;");
        asm("pop %rdi; ret;");
}

void win(unsigned long passme)
{
        char buf[0x30];

        // keep your filters
        if (passme != 0xcacacacacacacaca) {
                write(1, "Too bad, try again!", 19);
                return;
        }

        int fd = open("flag.txt", O_RDONLY);
        if (fd < 0) return;

        ssize_t n = read(fd, buf, sizeof(buf));
        if (n <= 0) return;

        write(1, buf, n);
}

void vuln(void)
{
        char vuln_buf[32];
        printf("Give it a shot -> ");
        read(0, vuln_buf, 56);
}

int main()
{
        setvbuf(stdin, 0, _IONBF, 0);
        setvbuf(stdout, 0, _IONBF, 0);

        char *heap = malloc(0x100);
        if (!heap) {
                perror("malloc");
                exit(0);
        }
        printf("Your new stack: %p\n", heap);

        printf("Prepare your ROP chain: ");
        read(0, heap, 0x100);

        vuln();
        return 0;
}
