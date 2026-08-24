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
        char *heap1 = malloc(0x420); // 0x430
        char *guard = malloc(0x10);

        free(heap1);    // break
        getchar();
        return 0;
}
