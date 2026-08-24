#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
        Topic: ROP to system() with RDI points to 'cat flag.txt' (available on .data)
*/

static char hmmm[13] = "cat flag.txt";

__attribute__((constructor))
void init(void)
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    __asm__(
        "pop %rdi;"
        "ret;"
    );
}

void banner(void)
{
        puts("Welcome to rop3");
        puts("Your task is to ROP this binary to get the flag");
        printf("ROP me: ");
}

void win(void)
{
        system("file flag.txt");
}

int main(void)
{
        banner();

        char vuln_buf[32] = {0};
        read(0, vuln_buf, sizeof(vuln_buf) * 3);

        return 0;
}