#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
void init(void)
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void banner(void)
{
        puts("Your task is to do ret2libc attack!");
        printf("Goodluck > ");
}

int main(void)
{
        banner();
        char buf[32];
        fgets(buf, sizeof(buf), stdin);
        printf(buf);

        printf("Value: ");
        char vuln_buf[32];
        gets(vuln_buf);
        
        return 0;
}