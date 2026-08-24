#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

__attribute__((constructor))
void init(void)
{
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	setbuf(stderr, NULL);
}

void pwn(void)
{
        FILE *flag_fp = fopen("flag.txt", "r");
        if (!flag_fp) {
                perror("fopen: ");
                _exit(1);
        }

        char flag_buf[64];
        char buf[64];
        memset(buf, 0x0, sizeof(flag_buf));
        memset(buf, 0x0, sizeof(buf));
        fread(flag_buf, sizeof(flag_buf), sizeof(char), flag_fp);

        printf("what: ");
        read(0, buf, sizeof(buf) - 1);
        printf(buf);
}

int main(void)
{
        pwn();
        return 0;
}