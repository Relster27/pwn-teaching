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
        char flag_buf[0x30];
        if (passme == 0x1a1a1a1a10101010) {
                FILE *flag_fd = fopen("flag.txt", "r");
                if(!flag_fd) {
                        perror("fopen");
                        exit(0);
                }

                fread(flag_buf, sizeof(flag_buf), sizeof(char), flag_fd);
                printf("Free MBG for you: %s\n", flag_buf);
        } else {
                puts("Come back later");
        }
}

int main(void)
{
        char vuln_buf[32];
        printf("MBG for you: %p\n", &main);
        printf("pwnme> ");
        fgets(vuln_buf, 64, stdin);
        return 0;
}
