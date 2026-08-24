#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
        Topic: Ret2win with rdi checked with 0x67676767
*/

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
        puts("Welcome to rop1");
        puts("Your task is to ROP this binary to win()");
        printf("ROP me: ");
}

void win(long checker)
{
        if (checker == 0x67676767) {
                puts("Gratz! Moving on to the next level!");
                printf("Here's your flag: ");
                system("cat flag.txt");
        }

        _exit(0);
}

int main(void)
{
        banner();

        char vuln_buf[32] = {0};
        read(0, vuln_buf, sizeof(vuln_buf) * 3);

        return 0;
}
