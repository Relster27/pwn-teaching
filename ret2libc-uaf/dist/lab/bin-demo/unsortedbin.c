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
        int amount = 7;
        char *h[amount];        // tcache[0xa0]

        for (int i = 0; i < amount; i++) {
                h[i] = malloc(0x90);
        }

        char *unsorted_0x100 = malloc(0x90);    // unsorted[0xa0]
        
        char *guard1 = malloc(0x10);
        
        char *unsorted_0x420 = malloc(0x410);    // unsorted[0x420]

        char *guard2 = malloc(0x10);

        for (int i = 0; i < amount; i++) {
                free(h[i]);
        }
        free(unsorted_0x100);
        free(unsorted_0x420);

        getchar();
        return 0;
}

