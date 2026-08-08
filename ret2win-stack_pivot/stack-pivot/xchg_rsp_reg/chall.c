#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// gcc chall.c -o chall -fno-stack-protector -no-pie -z now

void gadget_1(void)
{
        asm("pop %rax; ret;");
        asm("xchg %rax, %rsp; ret;");
}

void gadget_2(void)
{
        asm("pop %rdi; ret;");
        asm("pop %rsi; ret;");
        asm("pop %rdx; ret;");
}

void win(unsigned long filter_1, unsigned long filter_2, unsigned long filter_3)
{
        char buf[0x60];

        // keep your filters
        if (filter_1 != 0xdeadbeef || filter_2 != 0xcafebabe || filter_3 != 0x2badf00d) {
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
        char buf[32];

        printf("Input: ");
        read(0, buf, 64);  // overflow
}

int main(void)
{
        setbuf(stdout, NULL);
        setbuf(stdin, NULL);

        // Fake stack location
        void *heap = malloc(0x100);

        printf("Heap buffer at: %p\n", heap);

        printf("Prepare your ROP chain: ");
        read(0, heap, 0x100);   // stage 1: fake stack

        puts("Now overflow");
        vuln();                 // stage 2: pivot trigger

        return 0;
}
