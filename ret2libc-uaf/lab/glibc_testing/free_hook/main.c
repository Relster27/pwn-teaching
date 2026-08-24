#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))
void init(void)
{
        setbuf(stdin, NULL);
        setbuf(stdout, NULL);
        setbuf(stderr, NULL);
}

int main(void)
{
        char *heap = malloc(0x20);
        // strcpy(heap, "cat flag.txt");
        strcpy(heap, "/bin/sh");

        getchar();      // ubah value dari __free_hook ke system

        free(heap); // system(heap)

        // getchar();
        return 0;
}

