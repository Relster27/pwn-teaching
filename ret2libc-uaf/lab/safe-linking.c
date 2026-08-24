#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stdin, NULL);
}

int main(void)
{
        char *pointer = malloc(0x10);
        char *pointer1 = malloc(0x10);

        free(pointer);
        free(pointer1);

        getchar();
        return 0;
}
