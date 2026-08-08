// gcc chall.c -o chall -fno-stack-protector -fPIE -pie -Wl,-z,relro,-z,now -z noexecstack -O0

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
static void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stderr, NULL);
        __asm__("pop %rdi; ret;");
}

static void vuln(void)
{
        char buf[40];

        printf("Say something: ");
        read(0, buf, 0x100);
        puts("Thanks.");
}

int main(void)
{
        puts("=== yet another ret2libc with extra step ===");
        puts("One small hint is enough, right?");
        printf("hint: main is at %p\n", main);
        vuln();
        return 0;
}
