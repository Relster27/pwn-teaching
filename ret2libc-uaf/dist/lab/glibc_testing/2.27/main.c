#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stderr, NULL);
}

int main(void)
{
        // Before Safe Linking
        char *heap = malloc(0x10);
        char *heap1 = malloc(0x10);
        free(heap);
        free(heap1);

        return 0;
}
