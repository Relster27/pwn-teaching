#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        __asm__("pop %rdi; ret;");
}

void win(long long passme)
{
        char flag_buf[0x20];
        if (passme == 0x1337cafe) {
                FILE *flag_fd = fopen("flag.txt", "r");
                if(!flag_fd) {
                        perror("fopen");
                        exit(0);
                }

                fread(flag_buf, sizeof(flag_buf), sizeof(char), flag_fd);
                printf("Gratz! Here's your flag: %s\n", flag_buf);
        } else {
                puts("Nope! Bye-bye.");
        }
}

int main(void)
{
        char vuln_buf[32];
        printf("pwnme> ");
        fgets(vuln_buf, 64, stdin);
        return 0;
}
