#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stderr, NULL, _IONBF, 0);
        __asm__(
                "pop %rdi;"
                "ret;"
        );
}

void vuln(void)
{
        char buffer[20];
        gets(buffer);           // <- Buffer overflow vulnerability
        puts("Leaving!\n");     // <- Critical: provides output channel for our leak
}

int main(void) {
        puts("Good luck with this challenge!");
        printf(">> ");
        vuln();
        return 0;
}
