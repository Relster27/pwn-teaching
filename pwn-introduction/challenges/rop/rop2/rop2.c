#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
        Topic: Ret2win with RDI & RSI being checked, and the gadget is popping RSI first followed by RDI next.
*/

__attribute__((constructor))
void init(void)
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    __asm__(
        "pop %rsi;"
        "pop %rdi;"
        "ret;"
    );
}


void banner(void)
{
        puts("Welcome to rop2");
        puts("Your task is to ROP this binary to win()");
        printf("ROP me: ");
}

void win(long checker1, long checker2)
{
        if (checker1 == 0xffeeffee && checker2 == 0xccddccdd) {
                FILE *flag_fp = fopen("flag.txt", "r");
                if (!flag_fp) {
                        perror("fopen: ");
                        _exit(1);
                }
                char flag_buf[64] = {0};
                fread(flag_buf, sizeof(flag_buf), sizeof(char), flag_fp);

                puts("Gratz! Moving on to the next level!");
                printf("Here's your flag: ");
                puts(flag_buf);
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