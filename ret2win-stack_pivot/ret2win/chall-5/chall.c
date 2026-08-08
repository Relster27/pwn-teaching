#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        __asm__("pop %rdi; ret;");
        __asm__("pop %rsi; ret;");
}

void win(long long passme1, long long passme2)
{
        char flag_buf[0x30];
        if (passme1 == 0xd0d0 && passme2 == 0xc0c0) {
                FILE *flag_fd = fopen("flag.txt", "r");
                if(!flag_fd) {
                        perror("fopen");
                        exit(0);
                }

                fread(flag_buf, sizeof(flag_buf), sizeof(char), flag_fd);
                printf("Flag: %s\n", flag_buf);
        } else {
                puts("NT!");
        }
}

int main(void)
{
        char vuln_buf[32];
        printf("pwnme> ");
        fgets(vuln_buf, 80, stdin);
        return 0;
}
