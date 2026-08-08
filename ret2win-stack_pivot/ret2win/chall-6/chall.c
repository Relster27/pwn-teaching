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
        __asm__("pop %rdx; ret;");
}

void win(long long passme1, long long passme2, long long passme3)
{
        char flag_buf[0x30];
        if (passme1 == 0x12345678abcdef00 && passme2 == 0xcdcdcdcdcdcdcdcd && passme3 == 0xb19b055) {
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
        printf("A gift for a noble %p\n", win);

        char vuln_buf[32];
        printf("pwnme> ");
        fgets(vuln_buf, 128, stdin);
        return 0;
}
