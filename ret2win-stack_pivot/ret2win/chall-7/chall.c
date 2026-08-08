#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        __asm__("nop;");
}

void win(int passme1)
{
        char flag_buf[0x40];
        if (passme1 == 0x505505) {
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

void vuln()
{
        char vuln_buf[16];
        printf("pwnme> ");
        fgets(vuln_buf, 64, stdin);
}

int main(void)
{
        vuln();
        return 0;
}
